package com.lumbre.hotel.data

import com.lumbre.hotel.data.firebase.FirebaseAuthApi
import com.lumbre.hotel.data.firebase.FirebaseConfig
import com.lumbre.hotel.data.firebase.FirebaseException
import com.lumbre.hotel.data.firebase.FirestoreApi
import com.lumbre.hotel.data.firebase.Mappers
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.platform.systemLanguageTag
import com.russhwolf.settings.Settings
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.datetime.DateTimeUnit
import kotlinx.datetime.LocalDate
import kotlinx.datetime.TimeZone
import kotlinx.datetime.plus
import kotlinx.datetime.todayIn
import kotlinx.serialization.json.Json
import kotlin.random.Random
import kotlin.time.Clock
import kotlin.time.TimeSource

fun today(): LocalDate = Clock.System.todayIn(TimeZone.currentSystemDefault())
fun nowMs(): Long = Clock.System.now().toEpochMilliseconds()

/**
 * Única fuente de datos de la app, compartida por Android, iOS y web.
 *
 * Dos modos:
 * - **Nube** (Firebase configurado): cuentas con correo y contraseña, roles, y los datos viven en
 *   Cloud Firestore, así que el usuario recupera su información en cualquier dispositivo.
 * - **Local**: sin cuenta, los datos se guardan en el dispositivo (SharedPreferences, NSUserDefaults
 *   o localStorage). Las reservas hechas sin sesión se suben al iniciar sesión.
 *
 * Todo se expone como flujos reactivos: un cambio hecho desde el panel se refleja al momento
 * en las pantallas que lo observan.
 */
class HotelRepository(private val store: Settings = Settings()) {

    private val json = Json { ignoreUnknownKeys = true; encodeDefaults = true }
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

    val cloud: Boolean get() = FirebaseConfig.enabled

    // ---------- Estado ----------
    private val _prefs = MutableStateFlow(load(KEY_PREFS) { detectPrefs() })
    val prefs: StateFlow<Prefs> = _prefs.asStateFlow()

    private val _rooms = MutableStateFlow(load(KEY_ROOMS) { defaultRooms })
    val rooms: StateFlow<List<RoomConfig>> = _rooms.asStateFlow()

    private val _promos = MutableStateFlow(load(KEY_PROMOS) { defaultPromos })
    val promos: StateFlow<List<PromoCode>> = _promos.asStateFlow()

    private val _reservations = MutableStateFlow(load(KEY_RES) { if (cloud) emptyList() else seedReservations() })
    val reservations: StateFlow<List<Reservation>> = _reservations.asStateFlow()

    private val _params = MutableStateFlow(load(KEY_PARAMS) { Params() })
    val params: StateFlow<Params> = _params.asStateFlow()

    private val _account = MutableStateFlow<Account?>(load<Account?>(KEY_ACCOUNT) { null })
    val account: StateFlow<Account?> = _account.asStateFlow()

    private val _users = MutableStateFlow<List<Account>>(emptyList())
    val users: StateFlow<List<Account>> = _users.asStateFlow()

    private val _audit = MutableStateFlow<List<AuditEntry>>(emptyList())
    val audit: StateFlow<List<AuditEntry>> = _audit.asStateFlow()

    private val _syncing = MutableStateFlow(false)
    val syncing: StateFlow<Boolean> = _syncing.asStateFlow()

    /** Mensajes para mostrar al usuario (errores de red o permisos al sincronizar). */
    private val _events = MutableSharedFlow<K>(extraBufferCapacity = 8)
    val events: SharedFlow<K> = _events.asSharedFlow()

    /** Rol efectivo: el de la cuenta en la nube, o el demo administrador en modo local (solo web). */
    val role: StateFlow<Role> = combine(_account, _prefs) { acc, p ->
        when {
            cloud -> acc?.takeIf { !it.disabled }?.role ?: Role.GUEST
            p.admin && Capabilities.adminPanel -> Role.SUPERADMIN
            else -> Role.GUEST
        }
    }.stateIn(scope, SharingStarted.Eagerly, Role.GUEST)

    // ---------- Sesión ----------
    private var idToken: String? = null
    private var tokenExpiresAt: Long = 0
    private var refreshToken: String? = store.getStringOrNull(KEY_REFRESH)
    private val fs = FirestoreApi { validToken() }
    private var lastBooking: TimeSource.Monotonic.ValueTimeMark? = null

    init {
        if (_prefs.value.region == null) detectPrefs().region?.let { r -> _prefs.update { it.copy(region = r) } }
        if (cloud) scope.launch {
            pullPublic()
            if (refreshToken != null && validToken() != null) afterLogin() else if (refreshToken != null) signOutLocal()
        }
    }

    private suspend fun validToken(): String? {
        val rt = refreshToken ?: return null
        if (idToken != null && nowMs() < tokenExpiresAt - 60_000) return idToken
        return runCatching {
            val t = FirebaseAuthApi.refresh(rt)
            idToken = t.idToken; tokenExpiresAt = nowMs() + t.expiresInSec * 1000
            refreshToken = t.refreshToken; store.putString(KEY_REFRESH, t.refreshToken)
            idToken
        }.getOrNull()
    }

    // ---------- Preferencias ----------
    fun setLang(lang: Lang) = editPrefs(push = true) { it.copy(lang = lang) }
    fun setCurrency(currency: Currency) = editPrefs(push = true) { it.copy(currency = currency) }
    fun setTheme(mode: ThemeMode) = editPrefs(push = true) { it.copy(theme = mode) }
    fun markRegionNoticeShown() = editPrefs { it.copy(regionNoticeShown = true) }

    fun setConsent(consent: Consent) = editPrefs { it.copy(consent = consent.copy(decided = true, decidedAt = nowMs())) }

    /** Aplica idioma y moneda a partir del país detectado por ubicación (solo con consentimiento). */
    fun applyCountry(countryCode: String) {
        val p = detectPrefs("x-$countryCode")
        val lang = regionLang[countryCode.uppercase()] ?: _prefs.value.lang
        editPrefs(push = true) { it.copy(region = countryCode.uppercase(), lang = lang, currency = p.currency) }
    }

    /** Modo administrador de demostración: solo sin Firebase y solo en la web. */
    fun setAdmin(enabled: Boolean) {
        if (cloud || (enabled && !Capabilities.adminPanel)) return
        editPrefs { it.copy(admin = enabled) }
    }

    private fun editPrefs(push: Boolean = false, change: (Prefs) -> Prefs) {
        _prefs.update(change); save(KEY_PREFS, _prefs.value)
        val acc = _account.value
        if (push && cloud && acc != null) remote {
            val p = _prefs.value
            fs.update("users/${acc.uid}", mapOf("lang" to p.lang.name, "currency" to p.currency.name, "theme" to p.theme.name))
        }
    }

    // ---------- Cuentas ----------
    private val failedLogins get() = store.getInt(KEY_FAILS, 0)
    private val lockedUntil get() = store.getLong(KEY_LOCK, 0)

    /** Segundos que quedan de bloqueo por intentos fallidos (0 si no hay bloqueo). */
    fun lockoutRemainingSec(): Int = ((lockedUntil - nowMs()) / 1000).toInt().coerceAtLeast(0)

    /** Registra una cuenta nueva como huésped. Devuelve null si todo fue bien o la clave del error. */
    suspend fun register(name: String, email: String, phone: String, password: String): K? {
        if (!cloud) return K.E_NO_CLOUD
        return guarded {
            val t = FirebaseAuthApi.signUp(email.trim(), password)
            setSession(t.idToken, t.refreshToken, t.expiresInSec)
            val now = nowMs()
            val p = _prefs.value
            fs.set("users/${t.uid}", mapOf(
                "email" to t.email, "name" to name.trim(), "phone" to phone.trim(), "role" to Role.GUEST.name,
                "disabled" to false, "createdAt" to now, "lastLogin" to now,
                "lang" to p.lang.name, "currency" to p.currency.name, "theme" to p.theme.name,
            ))
            runCatching { FirebaseAuthApi.sendEmailVerification(t.idToken) }
            afterLogin()
        }
    }

    suspend fun login(email: String, password: String): K? {
        if (!cloud) return K.E_NO_CLOUD
        if (lockoutRemainingSec() > 0) return K.E_LOCKED
        val result = guarded {
            val t = FirebaseAuthApi.signIn(email.trim(), password)
            setSession(t.idToken, t.refreshToken, t.expiresInSec)
            afterLogin()
        }
        if (result == K.E_BAD_LOGIN) {
            val fails = failedLogins + 1
            store.putInt(KEY_FAILS, fails)
            if (fails >= _params.value.maxLoginAttempts) {
                store.putLong(KEY_LOCK, nowMs() + _params.value.lockoutSec * 1000L); store.putInt(KEY_FAILS, 0)
                return K.E_LOCKED
            }
        } else if (result == null) store.putInt(KEY_FAILS, 0)
        return result
    }

    suspend fun resetPassword(email: String): K? = guarded { FirebaseAuthApi.sendPasswordReset(email.trim()) }

    suspend fun changePassword(newPassword: String): K? = guarded {
        val token = validToken() ?: throw FirebaseException("TOKEN_EXPIRED")
        val t = FirebaseAuthApi.changePassword(token, newPassword)
        setSession(t.idToken, t.refreshToken, t.expiresInSec)
    }

    suspend fun resendVerification(): K? = guarded {
        FirebaseAuthApi.sendEmailVerification(validToken() ?: throw FirebaseException("TOKEN_EXPIRED"))
    }

    suspend fun updateProfile(name: String, phone: String): K? {
        val acc = _account.value ?: return K.E_PERMISSION
        return guarded {
            fs.update("users/${acc.uid}", mapOf("name" to name.trim(), "phone" to phone.trim()))
            setAccount(acc.copy(name = name.trim(), phone = phone.trim()))
        }
    }

    /** Elimina el perfil y la cuenta de autenticación (derecho de supresión). */
    suspend fun deleteAccount(): K? {
        val acc = _account.value ?: return K.E_PERMISSION
        return guarded {
            val token = validToken() ?: throw FirebaseException("TOKEN_EXPIRED")
            fs.delete("users/${acc.uid}")
            FirebaseAuthApi.deleteAccount(token)
            signOutLocal()
        }
    }

    fun logout() = signOutLocal()

    private fun setSession(id: String, refresh: String, expiresIn: Long) {
        idToken = id; tokenExpiresAt = nowMs() + expiresIn * 1000
        refreshToken = refresh; store.putString(KEY_REFRESH, refresh)
    }

    private fun setAccount(acc: Account?) {
        _account.value = acc
        if (acc == null) store.remove(KEY_ACCOUNT) else save(KEY_ACCOUNT, acc)
    }

    private fun signOutLocal() {
        idToken = null; refreshToken = null; tokenExpiresAt = 0
        store.remove(KEY_REFRESH); setAccount(null)
        _users.value = emptyList(); _audit.value = emptyList()
        _reservations.update { list -> list.filter { it.uid.isEmpty() } }
        save(KEY_RES, _reservations.value)
    }

    /** Tras iniciar sesión: perfil, preferencias, reservas locales pendientes y datos según el rol. */
    private suspend fun afterLogin() {
        val token = validToken() ?: return
        val uid = refreshUid() ?: return
        val doc = fs.get("users/$uid") ?: throw FirebaseException("PROFILE_MISSING")
        val verified = runCatching { FirebaseAuthApi.isEmailVerified(token) }.getOrDefault(false)
        val acc = Mappers.account(doc, verified)
        if (acc.disabled) { signOutLocal(); throw FirebaseException("USER_DISABLED") }
        setAccount(acc)
        // Preferencias guardadas en la nube: se recuperan en cualquier dispositivo.
        val f = doc.fields
        _prefs.update { p ->
            p.copy(
                lang = Lang.entries.firstOrNull { it.name == f["lang"] } ?: p.lang,
                currency = Currency.entries.firstOrNull { it.name == f["currency"] } ?: p.currency,
                theme = ThemeMode.entries.firstOrNull { it.name == f["theme"] } ?: p.theme,
            )
        }
        save(KEY_PREFS, _prefs.value)
        runCatching { fs.update("users/$uid", mapOf("lastLogin" to nowMs())) }
        // Reservas hechas sin sesión en este dispositivo: se suben a la cuenta.
        _reservations.value.filter { it.mine && it.uid.isEmpty() }.forEach { r ->
            runCatching { fs.set("reservations/${r.ref}", Mappers.reservationToFields(r.copy(uid = uid))) }
        }
        refreshAll()
    }

    private suspend fun refreshUid(): String? = _account.value?.uid ?: run {
        // El UID viene dentro del token JWT; se lee de forma segura sin librerías externas.
        val token = idToken ?: return null
        val payload = token.split('.').getOrNull(1) ?: return null
        val decoded = runCatching { base64UrlDecode(payload) }.getOrNull() ?: return null
        Regex("\"user_id\"\\s*:\\s*\"([^\"]+)\"").find(decoded)?.groupValues?.get(1)
    }

    /** Vuelve a descargar todo lo que el rol actual puede ver. */
    suspend fun refreshAll() {
        if (!cloud) return
        _syncing.value = true
        try {
            pullPublic()
            val acc = _account.value ?: return
            val docs = if (acc.role.atLeast(Role.STAFF)) fs.list("reservations") else fs.whereEquals("reservations", "uid", acc.uid)
            val remote = docs.mapNotNull { Mappers.reservation(it, acc.uid) }
            val localOnly = _reservations.value.filter { it.uid.isEmpty() && remote.none { r -> r.ref == it.ref } }
            _reservations.value = (remote + localOnly).sortedByDescending { it.checkIn }
            save(KEY_RES, _reservations.value)
            if (acc.role == Role.SUPERADMIN) {
                _users.value = fs.list("users").map { Mappers.account(it) }.sortedBy { it.email }
                _audit.value = fs.list("audit").map { Mappers.audit(it) }.sortedByDescending { it.at }.take(300)
                seedIfEmpty()
            }
        } catch (e: Throwable) {
            _events.tryEmit(mapError(e))
        } finally {
            _syncing.value = false
        }
    }

    private suspend fun pullPublic() {
        runCatching {
            val rooms = fs.list("rooms").mapNotNull { Mappers.room(it) }
            if (rooms.isNotEmpty()) {
                _rooms.value = RoomId.entries.map { id -> rooms.firstOrNull { it.id == id } ?: defaultRooms.first { it.id == id } }
                save(KEY_ROOMS, _rooms.value)
            }
            val promos = fs.list("promos").map { Mappers.promo(it) }
            if (promos.isNotEmpty()) { _promos.value = promos; save(KEY_PROMOS, promos) }
            fs.get("config/params")?.let { _params.value = Mappers.params(it); save(KEY_PARAMS, _params.value) }
        }
    }

    /** La primera vez que entra el superusuario se publican los datos iniciales del hotel. */
    private suspend fun seedIfEmpty() {
        if (fs.list("rooms").isEmpty()) _rooms.value.forEach { fs.set("rooms/${it.id.name}", Mappers.roomToFields(it)) }
        if (fs.list("promos").isEmpty()) _promos.value.forEach { fs.set("promos/${it.code}", Mappers.promoToFields(it)) }
        if (fs.get("config/params") == null) fs.set("config/params", Mappers.paramsToFields(_params.value))
    }

    // ---------- Administración ----------
    fun room(id: RoomId): RoomConfig = _rooms.value.first { it.id == id }

    fun updateRoom(id: RoomId, nightlyEur: Int, available: Boolean) {
        require(Role.ADMIN)
        _rooms.update { list -> list.map { if (it.id == id) it.copy(nightlyEur = nightlyEur.coerceIn(30, 5000), available = available) else it } }
        save(KEY_ROOMS, _rooms.value)
        remote { fs.set("rooms/${id.name}", Mappers.roomToFields(room(id))); audit("ROOM_UPDATE", "${id.name} $nightlyEur€ $available") }
    }

    fun findPromo(code: String): PromoCode? =
        _promos.value.firstOrNull { it.active && it.code.equals(code.trim(), ignoreCase = true) }

    fun upsertPromo(promo: PromoCode) {
        require(Role.ADMIN)
        _promos.update { list -> list.filterNot { it.code == promo.code } + promo }
        save(KEY_PROMOS, _promos.value)
        remote { fs.set("promos/${promo.code}", Mappers.promoToFields(promo)); audit("PROMO_SAVE", "${promo.code} ${promo.percent}% ${promo.active}") }
    }

    fun deletePromo(code: String) {
        require(Role.ADMIN)
        _promos.update { list -> list.filterNot { it.code == code } }
        save(KEY_PROMOS, _promos.value)
        remote { fs.delete("promos/$code"); audit("PROMO_DELETE", code) }
    }

    fun setParams(p: Params) {
        require(Role.SUPERADMIN)
        _params.value = p; save(KEY_PARAMS, p)
        remote { fs.set("config/params", Mappers.paramsToFields(p)); audit("PARAMS_UPDATE", "tax=${p.taxPercent} maxNights=${p.maxNights}") }
    }

    fun setUserRole(uid: String, role: Role) {
        require(Role.SUPERADMIN)
        if (uid == _account.value?.uid) return
        _users.update { list -> list.map { if (it.uid == uid) it.copy(role = role) else it } }
        val email = _users.value.firstOrNull { it.uid == uid }?.email ?: uid
        remote { fs.update("users/$uid", mapOf("role" to role.name)); audit("ROLE_CHANGE", "$email → ${role.name}") }
    }

    fun setUserDisabled(uid: String, disabled: Boolean) {
        require(Role.SUPERADMIN)
        if (uid == _account.value?.uid) return
        _users.update { list -> list.map { if (it.uid == uid) it.copy(disabled = disabled) else it } }
        val email = _users.value.firstOrNull { it.uid == uid }?.email ?: uid
        remote { fs.update("users/$uid", mapOf("disabled" to disabled)); audit(if (disabled) "USER_BLOCK" else "USER_UNBLOCK", email) }
    }

    // ---------- Reservas ----------
    /** Devuelve null si se intenta reservar otra vez antes del tiempo de espera configurado. */
    fun book(draft: Reservation): Reservation? {
        lastBooking?.let { if (it.elapsedNow().inWholeSeconds < _params.value.bookingCooldownSec) return null }
        lastBooking = TimeSource.Monotonic.markNow()
        val acc = _account.value
        val saved = draft.copy(ref = newRef(), mine = true, status = ReservationStatus.CONFIRMED, uid = acc?.uid ?: "", createdAt = nowMs())
        _reservations.update { listOf(saved) + it }
        save(KEY_RES, _reservations.value)
        if (acc != null) remote { fs.set("reservations/${saved.ref}", Mappers.reservationToFields(saved)) }
        return saved
    }

    fun setStatus(ref: String, status: ReservationStatus) {
        val target = _reservations.value.firstOrNull { it.ref == ref } ?: return
        // El huésped solo puede cancelar las suyas; el resto lo hace recepción o superior.
        if (!(target.mine && status == ReservationStatus.CANCELLED)) require(Role.STAFF)
        _reservations.update { list -> list.map { if (it.ref == ref) it.copy(status = status) else it } }
        save(KEY_RES, _reservations.value)
        if (target.uid.isNotEmpty()) remote {
            fs.update("reservations/$ref", mapOf("status" to status.name))
            if (!target.mine) audit("RES_STATUS", "$ref → ${status.name}")
        }
    }

    fun clearMyData() {
        _reservations.update { list -> list.filterNot { it.mine && it.uid.isEmpty() } }
        save(KEY_RES, _reservations.value)
    }

    // ---------- Utilidades ----------
    private fun require(min: Role) {
        check(role.value.atLeast(min)) { "Permiso insuficiente: se requiere ${min.name}" }
    }

    private suspend fun audit(action: String, target: String) {
        val acc = _account.value ?: return
        runCatching { fs.add("audit", mapOf("at" to nowMs(), "actor" to acc.email, "action" to action, "target" to target.take(120))) }
        if (acc.role == Role.SUPERADMIN) _audit.update { listOf(AuditEntry(nowMs(), acc.email, action, target)) + it }
    }

    /** Ejecuta una escritura en la nube en segundo plano; si falla, avisa y vuelve a sincronizar. */
    private fun remote(block: suspend () -> Unit) {
        if (!cloud || _account.value == null) return
        scope.launch {
            try { block() } catch (e: Throwable) { _events.tryEmit(mapError(e)); refreshAll() }
        }
    }

    private suspend fun guarded(block: suspend () -> Unit): K? = try {
        block(); null
    } catch (e: Throwable) {
        mapError(e)
    }

    private fun mapError(e: Throwable): K = when ((e as? FirebaseException)?.code) {
        null -> K.E_NETWORK
        "EMAIL_EXISTS" -> K.E_EMAIL_EXISTS
        "EMAIL_NOT_FOUND", "INVALID_PASSWORD", "INVALID_LOGIN_CREDENTIALS", "INVALID_EMAIL" -> K.E_BAD_LOGIN
        "USER_DISABLED" -> K.E_DISABLED
        "TOO_MANY_ATTEMPTS_TRY_LATER" -> K.E_TOO_MANY
        "WEAK_PASSWORD" -> K.E_WEAK
        "PERMISSION_DENIED" -> K.E_PERMISSION
        "TOKEN_EXPIRED", "INVALID_ID_TOKEN", "CREDENTIAL_TOO_OLD_LOGIN_AGAIN", "USER_NOT_FOUND" -> K.E_SESSION
        else -> K.E_NETWORK
    }

    private inline fun <reified T> load(key: String, default: () -> T): T =
        store.getStringOrNull(key)?.let { runCatching { json.decodeFromString<T>(it) }.getOrNull() } ?: default()

    private inline fun <reified T> save(key: String, value: T) = store.putString(key, json.encodeToString(value))

    private fun newRef(): String {
        val alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "LMB-" + (1..6).map { alphabet[Random.nextInt(alphabet.length)] }.joinToString("")
    }

    private fun seedReservations(): List<Reservation> {
        val t = today()
        fun r(ref: String, name: String, room: RoomId, inDays: Int, nights: Int, a: Int, c: Int, total: Double, st: ReservationStatus) =
            Reservation(ref, name, name.lowercase().replace(' ', '.') + "@correo.com", "", room,
                t.plus(inDays, DateTimeUnit.DAY), t.plus(inDays + nights, DateTimeUnit.DAY), a, c, emptySet(), null, total, st)
        return listOf(
            r("LMB-7QK2PA", "Marta Gil", RoomId.DELUXE, -1, 4, 2, 0, 902.0, ReservationStatus.CHECKED_IN),
            r("LMB-H3XW9C", "James Carter", RoomId.PENTHOUSE, 3, 5, 4, 2, 2050.5, ReservationStatus.CONFIRMED),
            r("LMB-N8D4TR", "Camille Roux", RoomId.STANDARD, 7, 2, 2, 0, 290.4, ReservationStatus.CONFIRMED),
            r("LMB-5MZ7LE", "Rafael Souza", RoomId.DELUXE, 12, 7, 2, 1, 1310.0, ReservationStatus.CONFIRMED),
            r("LMB-B2V6YU", "Lucía Romero", RoomId.STANDARD, 0, 3, 1, 0, 396.0, ReservationStatus.CHECKED_IN),
            r("LMB-K9P3SG", "Ken Watanabe", RoomId.PENTHOUSE, 20, 3, 3, 0, 1188.0, ReservationStatus.CANCELLED),
        )
    }

    companion object {
        private const val KEY_PREFS = "lumbre.prefs.v1"
        private const val KEY_ROOMS = "lumbre.rooms.v1"
        private const val KEY_PROMOS = "lumbre.promos.v1"
        private const val KEY_RES = "lumbre.reservations.v2"
        private const val KEY_PARAMS = "lumbre.params.v1"
        private const val KEY_ACCOUNT = "lumbre.account.v1"
        private const val KEY_REFRESH = "lumbre.session.refresh"
        private const val KEY_FAILS = "lumbre.session.fails"
        private const val KEY_LOCK = "lumbre.session.lockedUntil"

        val defaultRooms = listOf(
            RoomConfig(RoomId.STANDARD, 120, 2),
            RoomConfig(RoomId.DELUXE, 190, 3),
            RoomConfig(RoomId.PENTHOUSE, 340, 6),
        )
        val defaultPromos = listOf(PromoCode("LUMBRE10", 10), PromoCode("VERANO15", 15, active = false))

        private val regionCurrency = mapOf("MX" to Currency.MXN, "US" to Currency.USD, "GB" to Currency.GBP, "BR" to Currency.BRL, "CO" to Currency.COP)
        private val euroZone = setOf("ES", "FR", "PT", "DE", "IT", "NL", "BE", "IE", "AT", "GR", "FI", "LU")
        val regionLang = mapOf(
            "ES" to Lang.ES, "MX" to Lang.ES, "CO" to Lang.ES, "AR" to Lang.ES, "CL" to Lang.ES, "PE" to Lang.ES,
            "US" to Lang.EN, "GB" to Lang.EN, "CA" to Lang.EN, "AU" to Lang.EN, "IE" to Lang.EN,
            "BR" to Lang.PT, "PT" to Lang.PT, "FR" to Lang.FR, "BE" to Lang.FR,
        )

        /** Idioma y moneda iniciales según el idioma y la región del dispositivo o navegador. */
        fun detectPrefs(tag: String = systemLanguageTag()): Prefs {
            val parts = tag.replace('_', '-').split('-')
            val language = parts.firstOrNull()?.lowercase()
            val region = parts.drop(1).firstOrNull { it.length == 2 && it.all(Char::isLetter) }?.uppercase()
            val lang = Lang.entries.firstOrNull { it.code == language } ?: regionLang[region] ?: Lang.EN
            val currency = regionCurrency[region] ?: if (region in euroZone || region == null) Currency.EUR else Currency.USD
            return Prefs(lang = lang, currency = currency, region = region)
        }

        private fun base64UrlDecode(s: String): String {
            val alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
            val clean = s.trimEnd('=')
            val bytes = ArrayList<Byte>()
            var buffer = 0; var bits = 0
            for (c in clean) {
                val v = alphabet.indexOf(c).takeIf { it >= 0 } ?: continue
                buffer = (buffer shl 6) or v; bits += 6
                if (bits >= 8) { bits -= 8; bytes.add(((buffer shr bits) and 0xFF).toByte()) }
            }
            return bytes.toByteArray().decodeToString()
        }
    }
}

/** Contenedor de dependencias mínimo: una sola instancia para toda la app. */
object AppGraph {
    val repo: HotelRepository by lazy { HotelRepository() }
}
