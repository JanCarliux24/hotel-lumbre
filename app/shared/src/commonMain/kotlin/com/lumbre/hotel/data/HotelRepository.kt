package com.lumbre.hotel.data

import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.platform.systemLanguageTag
import com.russhwolf.settings.Settings
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
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

/**
 * Única fuente de datos de la app, compartida por Android, iOS y web.
 *
 * Expone flujos reactivos: cuando el panel administrativo cambia un precio o el estado
 * de una reserva, todas las pantallas que lo observan se actualizan al momento.
 * Ahora persiste en el propio dispositivo (SharedPreferences, NSUserDefaults o
 * localStorage). Para sincronizar entre dispositivos basta con sustituir [store]
 * por un backend (Supabase, Firebase o una API propia) sin tocar la interfaz.
 */
class HotelRepository(private val store: Settings = Settings()) {

    private val json = Json { ignoreUnknownKeys = true; encodeDefaults = true }

    private val _prefs = MutableStateFlow(load(KEY_PREFS) { detectPrefs() })
    val prefs: StateFlow<Prefs> = _prefs.asStateFlow()

    private val _rooms = MutableStateFlow(load(KEY_ROOMS) { defaultRooms })
    val rooms: StateFlow<List<RoomConfig>> = _rooms.asStateFlow()

    private val _promos = MutableStateFlow(load(KEY_PROMOS) { defaultPromos })
    val promos: StateFlow<List<PromoCode>> = _promos.asStateFlow()

    private val _reservations = MutableStateFlow(load(KEY_RES) { seedReservations() })
    val reservations: StateFlow<List<Reservation>> = _reservations.asStateFlow()

    private var lastBooking: TimeSource.Monotonic.ValueTimeMark? = null

    init {
        // Si aún no conocemos la región (preferencias antiguas), se vuelve a detectar sin tocar idioma ni moneda.
        if (_prefs.value.region == null) detectPrefs().region?.let { r -> _prefs.update { it.copy(region = r) } }
    }

    // ---------- Preferencias ----------
    fun setLang(lang: Lang) = editPrefs { it.copy(lang = lang) }
    fun setCurrency(currency: Currency) = editPrefs { it.copy(currency = currency) }
    fun markRegionNoticeShown() = editPrefs { it.copy(regionNoticeShown = true) }

    /** Solo la web puede abrir una sesión administrativa. */
    fun setAdmin(enabled: Boolean) {
        if (enabled && !Capabilities.adminPanel) return
        editPrefs { it.copy(admin = enabled) }
    }

    private fun editPrefs(change: (Prefs) -> Prefs) {
        _prefs.update(change); save(KEY_PREFS, _prefs.value)
    }

    // ---------- Habitaciones y promociones (administración) ----------
    fun room(id: RoomId): RoomConfig = _rooms.value.first { it.id == id }

    fun updateRoom(id: RoomId, nightlyEur: Int, available: Boolean) {
        requireAdmin()
        _rooms.update { list -> list.map { if (it.id == id) it.copy(nightlyEur = nightlyEur.coerceIn(30, 5000), available = available) else it } }
        save(KEY_ROOMS, _rooms.value)
    }

    fun findPromo(code: String): PromoCode? =
        _promos.value.firstOrNull { it.active && it.code.equals(code.trim(), ignoreCase = true) }

    fun upsertPromo(promo: PromoCode) {
        requireAdmin()
        _promos.update { list -> list.filterNot { it.code == promo.code } + promo }
        save(KEY_PROMOS, _promos.value)
    }

    fun deletePromo(code: String) {
        requireAdmin()
        _promos.update { list -> list.filterNot { it.code == code } }
        save(KEY_PROMOS, _promos.value)
    }

    // ---------- Reservas ----------
    /** Devuelve null si se intenta reservar otra vez en menos de 20 s (anti-abuso). */
    fun book(draft: Reservation): Reservation? {
        lastBooking?.let { if (it.elapsedNow().inWholeSeconds < 20) return null }
        lastBooking = TimeSource.Monotonic.markNow()
        val saved = draft.copy(ref = newRef(), mine = true, status = ReservationStatus.CONFIRMED)
        _reservations.update { listOf(saved) + it }
        save(KEY_RES, _reservations.value)
        return saved
    }

    fun setStatus(ref: String, status: ReservationStatus) {
        val target = _reservations.value.firstOrNull { it.ref == ref } ?: return
        // El huésped solo puede cancelar las suyas; el resto de cambios es administrativo.
        if (!(target.mine && status == ReservationStatus.CANCELLED)) requireAdmin()
        _reservations.update { list -> list.map { if (it.ref == ref) it.copy(status = status) else it } }
        save(KEY_RES, _reservations.value)
    }

    fun clearMyData() {
        _reservations.update { list -> list.filterNot { it.mine } }
        save(KEY_RES, _reservations.value)
    }

    private fun requireAdmin() {
        check(Capabilities.adminPanel && _prefs.value.admin) { "Acción solo disponible para administración en la web" }
    }

    // ---------- Persistencia ----------
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
        private const val KEY_RES = "lumbre.reservations.v1"

        val defaultRooms = listOf(
            RoomConfig(RoomId.STANDARD, 120, 2),
            RoomConfig(RoomId.DELUXE, 190, 3),
            RoomConfig(RoomId.PENTHOUSE, 340, 6),
        )
        val defaultPromos = listOf(PromoCode("LUMBRE10", 10), PromoCode("VERANO15", 15, active = false))

        private val regionCurrency = mapOf("MX" to Currency.MXN, "US" to Currency.USD, "GB" to Currency.GBP, "BR" to Currency.BRL, "CO" to Currency.COP)
        private val regionLang = mapOf(
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
            val currency = regionCurrency[region] ?: Currency.EUR
            return Prefs(lang = lang, currency = currency, region = region)
        }
    }
}

/** Contenedor de dependencias mínimo: una sola instancia para toda la app. */
object AppGraph {
    val repo: HotelRepository by lazy { HotelRepository() }
}
