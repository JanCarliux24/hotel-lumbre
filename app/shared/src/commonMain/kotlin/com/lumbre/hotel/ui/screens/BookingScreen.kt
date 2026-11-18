package com.lumbre.hotel.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.CalendarMonth
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.ExpandLess
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material.icons.rounded.LocalOffer
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.Extra
import com.lumbre.hotel.data.PromoCode
import com.lumbre.hotel.data.Reservation
import com.lumbre.hotel.data.RoomConfig
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.data.today
import com.lumbre.hotel.domain.Format
import com.lumbre.hotel.domain.LineKind
import com.lumbre.hotel.domain.Pricing
import com.lumbre.hotel.domain.Quote
import com.lumbre.hotel.domain.QuoteLine
import com.lumbre.hotel.domain.Validation
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.nights
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.ui.components.AnimatedMoney
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.ConfettiBurst
import com.lumbre.hotel.ui.components.LocalWide
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.LumiSays
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.Mood
import com.lumbre.hotel.ui.components.Stepper
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.bounceClick
import com.lumbre.hotel.ui.components.money
import com.lumbre.hotel.ui.navigation.BookingRoute
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlinx.coroutines.delay
import kotlinx.datetime.DateTimeUnit
import kotlinx.datetime.LocalDate
import kotlinx.datetime.daysUntil
import kotlinx.datetime.plus
import org.jetbrains.compose.resources.painterResource

/** Estado del formulario de reserva (vive mientras la pantalla está abierta). */
private class BookingState(route: BookingRoute, today: LocalDate, rooms: List<RoomConfig>) {
    var step by mutableIntStateOf(1)
    var checkIn by mutableStateOf(route.checkIn?.let { runCatching { LocalDate.parse(it) }.getOrNull() } ?: today.plus(14, DateTimeUnit.DAY))
    var checkOut by mutableStateOf(route.checkOut?.let { runCatching { LocalDate.parse(it) }.getOrNull() } ?: today.plus(17, DateTimeUnit.DAY))
    var adults by mutableIntStateOf(route.guests.coerceIn(1, 6))
    var children by mutableIntStateOf(0)
    var room by mutableStateOf(
        RoomId.entries.firstOrNull { it.name == route.room }
            ?: rooms.firstOrNull { it.available && it.capacity >= route.guests && it.id != RoomId.STANDARD }?.id
            ?: rooms.firstOrNull { it.available && it.capacity >= route.guests }?.id
            ?: RoomId.DELUXE
    )
    var extras by mutableStateOf(setOf<Extra>())
    var promoInput by mutableStateOf("")
    var promo by mutableStateOf<PromoCode?>(null)
    var promoError by mutableStateOf<K?>(null)
    var name by mutableStateOf("")
    var email by mutableStateOf("")
    var phone by mutableStateOf("")
    var notes by mutableStateOf("")
    var consent by mutableStateOf(false)
    var formError by mutableStateOf<K?>(null)
    /** Pasos en los que ya se intentó continuar (a partir de ahí se muestran los errores). */
    val tried = mutableStateMapOf<Int, Boolean>()
    /** Campos que el usuario ya visitó y abandonó. */
    val touched = mutableStateMapOf<String, Boolean>()

    val guests: Int get() = adults + children
    fun show(step: Int, field: String) = tried[step] == true || touched[field] == true
}

@Composable
fun BookingScreen(route: BookingRoute, onClose: () -> Unit, onTrips: () -> Unit, onHome: () -> Unit) {
    val repo = AppGraph.repo
    val rooms by repo.rooms.collectAsState()
    val today = remember { today() }
    val s = remember { BookingState(route, today, repo.rooms.value) }
    val wide = LocalWide.current
    val haptic = LocalHapticFeedback.current
    var confirmed by remember { mutableStateOf<Reservation?>(null) }

    var lumiKey by remember { mutableStateOf(K.L_1) }
    var lumiMood by remember { mutableStateOf(Mood.Happy) }
    var lumiTick by remember { mutableIntStateOf(0) }
    fun say(k: K, mood: Mood) { lumiKey = k; lumiMood = mood; lumiTick++ }

    val roomCfg = rooms.first { it.id == s.room }
    val dateError = Validation.dates(s.checkIn, s.checkOut, today)
    val quote: Quote? = if (dateError == null) Pricing.quote(roomCfg, s.checkIn, s.checkOut, s.adults, s.children, s.extras, s.promo?.percent ?: 0) else null

    LaunchedEffect(quote?.hasLongStay) { if (quote?.hasLongStay == true && s.step == 1) say(K.L_LONG, Mood.Party) }

    fun roomError(): K? = when {
        !roomCfg.available -> K.E_UNAVAILABLE
        s.guests > roomCfg.capacity -> K.E_CAPACITY
        else -> null
    }

    fun applyPromo(silent: Boolean = false): Boolean {
        val code = s.promoInput.trim().uppercase()
        s.promoInput = code
        if (code.isEmpty()) { s.promo = null; s.promoError = null; return true }
        val found = repo.findPromo(code)
        return if (found == null) {
            s.promo = null; s.promoError = K.E_PROMO; false
        } else {
            val isNew = s.promo?.code != found.code
            s.promo = found; s.promoError = null
            if (isNew && !silent) say(K.L_PROMO, Mood.Party)
            true
        }
    }

    fun validate(step: Int): Boolean {
        s.tried[step] = true
        return when (step) {
            1 -> dateError == null
            2 -> listOf(roomError() == null, applyPromo(silent = true)).all { it }
            else -> listOf(
                Validation.name(s.name) == null, Validation.email(s.email) == null,
                Validation.phone(s.phone) == null, s.consent,
            ).all { it }
        }
    }

    fun next() {
        if (validate(s.step)) {
            s.step += 1
            say(if (s.step == 2) K.L_2 else K.L_3, Mood.Happy)
        } else {
            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
            say(K.L_ERR, Mood.Sad)
        }
    }

    fun confirm() {
        val okAll = (1..3).all { validate(it) }
        val q = quote
        if (!okAll || q == null) {
            s.step = (1..3).first { !validate(it) }.coerceAtLeast(1)
            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
            say(K.L_ERR, Mood.Sad); return
        }
        val saved = repo.book(
            Reservation(
                ref = "", guestName = s.name.trim().replace(Regex("\\s+"), " "), email = s.email.trim(), phone = s.phone.trim(),
                room = s.room, checkIn = s.checkIn, checkOut = s.checkOut, adults = s.adults, children = s.children,
                extras = s.extras, promo = s.promo?.code, totalEur = q.totalEur,
            )
        )
        if (saved == null) { s.formError = K.E_COOLDOWN; say(K.L_ERR, Mood.Sad); return }
        s.formError = null
        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
        confirmed = saved
    }

    confirmed?.let { res ->
        SuccessView(res, quote, onTrips, onHome)
        return
    }

    Column(Modifier.fillMaxSize().imePadding()) {
        // Barra superior + progreso
        MaxWidth(Modifier.statusBarsPadding().padding(horizontal = 12.dp, vertical = 8.dp)) {
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onClose) { Icon(Icons.Rounded.Close, t(K.CLOSE)) }
                    Text(t(K.BK_TITLE), style = MaterialTheme.typography.titleLarge, modifier = Modifier.weight(1f))
                }
                StepsBar(s.step, Modifier.padding(horizontal = 12.dp))
            }
        }

        val content: @Composable (Modifier) -> Unit = { mod ->
            Column(mod.verticalScroll(rememberScrollState()).padding(horizontal = 20.dp, vertical = 12.dp)) {
                LumiSays(t(lumiKey), lumiMood, trigger = lumiTick)
                Spacer(Modifier.height(20.dp))
                AnimatedContent(
                    targetState = s.step,
                    transitionSpec = {
                        val dir = if (targetState > initialState) 1 else -1
                        (slideInHorizontally(spring(dampingRatio = 0.85f, stiffness = 300f)) { it / 3 * dir } + fadeIn()) togetherWith
                            (slideOutHorizontally(tween(200)) { -it / 3 * dir } + fadeOut(tween(150)))
                    },
                    label = "step",
                ) { step ->
                    when (step) {
                        1 -> StepDates(s, dateError, today)
                        2 -> StepRoom(s, rooms, roomError(), ::applyPromo)
                        else -> StepDetails(s)
                    }
                }
            }
        }

        if (wide) {
            MaxWidth(Modifier.weight(1f), max = 1100.dp) {
                Row(Modifier.fillMaxSize().padding(horizontal = 12.dp)) {
                    Column(Modifier.weight(1.4f)) {
                        content(Modifier.weight(1f))
                        NavButtons(s.step, Modifier.padding(20.dp), onBack = { s.step -= 1; say(if (s.step == 1) K.L_1 else K.L_2, Mood.Happy) }, onNext = ::next, onConfirm = ::confirm)
                    }
                    Card(
                        Modifier.weight(1f).padding(12.dp),
                        shape = RoundedCornerShape(28.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
                        elevation = CardDefaults.cardElevation(4.dp),
                    ) { Column(Modifier.padding(24.dp)) { QuoteSummary(quote, s.room, expanded = true) } }
                }
            }
        } else {
            content(Modifier.weight(1f))
            Surface(
                color = MaterialTheme.colorScheme.surfaceContainerLowest, shadowElevation = 18.dp,
                shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
            ) {
                Column(Modifier.navigationBarsPadding().padding(horizontal = 20.dp, vertical = 14.dp)) {
                    QuoteSummary(quote, s.room, expanded = false)
                    Spacer(Modifier.height(12.dp))
                    NavButtons(s.step, Modifier, onBack = { s.step -= 1; say(if (s.step == 1) K.L_1 else K.L_2, Mood.Happy) }, onNext = ::next, onConfirm = ::confirm)
                }
            }
        }
    }
}

@Composable
private fun StepsBar(step: Int, modifier: Modifier = Modifier) {
    val labels = listOf(K.STEP_DATES, K.STEP_ROOM, K.STEP_DATA)
    Row(modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        labels.forEachIndexed { i, k ->
            val fill by animateFloatAsState(if (step > i) 1f else 0f, spring(dampingRatio = 0.6f, stiffness = 220f), label = "seg")
            Column(Modifier.weight(1f)) {
                Box(Modifier.fillMaxWidth().height(8.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
                    Box(Modifier.fillMaxWidth(fill).height(8.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary))
                }
                Spacer(Modifier.height(6.dp))
                Text(
                    t(k), style = MaterialTheme.typography.labelMedium,
                    color = if (step == i + 1) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun NavButtons(step: Int, modifier: Modifier, onBack: () -> Unit, onNext: () -> Unit, onConfirm: () -> Unit) {
    Row(modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        if (step > 1) LumbreButton(t(K.BACK), onBack, kind = BtnKind.Secondary)
        if (step < 3) LumbreButton(t(K.CONTINUE), onNext, Modifier.weight(1f))
        else LumbreButton(t(K.BOOK_CONFIRM), onConfirm, Modifier.weight(1f), kind = BtnKind.Gold, icon = Icons.Rounded.Check)
    }
}

@Composable
private fun StepDates(s: BookingState, dateError: K?, today: LocalDate) {
    val lang = LocalLang.current
    var picking by remember { mutableStateOf(false) }
    Column {
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            DateBox(t(K.CHECKIN), Format.shortDate(s.checkIn, lang), Modifier.weight(1f)) { picking = true }
            DateBox(t(K.CHECKOUT), Format.shortDate(s.checkOut, lang), Modifier.weight(1f)) { picking = true }
        }
        AnimatedVisibility(dateError != null && s.tried[1] == true) {
            Text(dateError?.let { t(it) } ?: "", color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall, modifier = Modifier.padding(top = 8.dp, start = 4.dp))
        }
        if (dateError == null) {
            Text(
                nights(lang, s.checkIn.daysUntil(s.checkOut)),
                style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.padding(top = 10.dp, start = 4.dp),
            )
        }
        Spacer(Modifier.height(28.dp))
        Stepper(t(K.ADULTS), null, s.adults, 1..6, { s.adults = it })
        Spacer(Modifier.height(16.dp))
        Stepper(t(K.CHILDREN), t(K.CHILDREN_HINT), s.children, 0..4, { s.children = it })
    }
    if (picking) {
        DateRangeDialog(s.checkIn, s.checkOut, onDismiss = { picking = false }) { a, b ->
            s.checkIn = a; s.checkOut = b; picking = false
        }
    }
}


@Composable
private fun DateBox(label: String, value: String, modifier: Modifier, onClick: () -> Unit) {
    Column(
        modifier.clip(RoundedCornerShape(20.dp)).background(MaterialTheme.colorScheme.surfaceContainerLowest)
            .border(1.dp, MaterialTheme.colorScheme.outlineVariant, RoundedCornerShape(20.dp))
            .bounceClick(scaleDown = 0.97f, onClick = onClick).padding(16.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Rounded.CalendarMonth, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
            Spacer(Modifier.width(6.dp))
            Text(label, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Spacer(Modifier.height(6.dp))
        Text(value, style = MaterialTheme.typography.titleLarge)
    }
}

@Composable
private fun StepRoom(s: BookingState, rooms: List<RoomConfig>, roomError: K?, applyPromo: (Boolean) -> Boolean) {
    Column {
        Text(t(K.STEP_ROOM), style = MaterialTheme.typography.titleLarge)
        Spacer(Modifier.height(12.dp))
        Catalog.rooms.forEachIndexed { i, info ->
            val cfg = rooms.first { it.id == info.id }
            val fits = cfg.available && cfg.capacity >= s.guests
            val selected = s.room == info.id
            val border by animateColorAsState(if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outlineVariant, label = "b")
            val pop = remember { Animatable(1f) }
            LaunchedEffect(selected) { if (selected) { pop.snapTo(0.97f); pop.animateTo(1f, spring(dampingRatio = 0.4f, stiffness = 400f)) } }
            Row(
                Modifier.fillMaxWidth().padding(bottom = 10.dp).appear(i)
                    .graphicsLayer { scaleX = pop.value; scaleY = pop.value; alpha = if (fits) 1f else 0.5f }
                    .clip(RoundedCornerShape(20.dp))
                    .background(if (selected) MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.5f) else MaterialTheme.colorScheme.surfaceContainerLowest)
                    .border(if (selected) 2.dp else 1.dp, border, RoundedCornerShape(20.dp))
                    .bounceClick(scaleDown = 0.98f) { s.room = info.id }
                    .padding(12.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Image(painterResource(info.image), null, contentScale = ContentScale.Crop, modifier = Modifier.size(72.dp).clip(RoundedCornerShape(14.dp)))
                Spacer(Modifier.width(14.dp))
                Column(Modifier.weight(1f)) {
                    Text(t(info.name), style = MaterialTheme.typography.titleMedium)
                    Text(
                        if (!cfg.available) t(K.UNAVAILABLE) else t(K.ROOM_MAX, cfg.capacity),
                        style = MaterialTheme.typography.bodySmall,
                        color = if (fits) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.error,
                    )
                }
                Column(horizontalAlignment = Alignment.End) {
                    Text(money(cfg.nightlyEur.toDouble()), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                    Text(t(K.PER_NIGHT), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
        val selectedCfg = rooms.first { it.id == s.room }
        AnimatedVisibility(roomError != null && s.tried[2] == true) {
            Text(roomError?.let { t(it, selectedCfg.capacity) } ?: "", color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
        }

        Spacer(Modifier.height(20.dp))
        Text(t(K.EXTRAS), style = MaterialTheme.typography.titleLarge)
        Spacer(Modifier.height(10.dp))
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Extra.entries.forEach { x ->
                val on = x in s.extras
                FilterChip(
                    selected = on,
                    onClick = { s.extras = if (on) s.extras - x else s.extras + x },
                    label = { Text("${t(Catalog.extraName(x))} · ${money(x.eur.toDouble())}/${t(Catalog.extraUnit(x))}") },
                    leadingIcon = if (on) ({ Icon(Icons.Rounded.Check, null, Modifier.size(18.dp)) }) else null,
                    shape = RoundedCornerShape(50),
                )
            }
        }

        Spacer(Modifier.height(24.dp))
        Row(verticalAlignment = Alignment.Top) {
            OutlinedTextField(
                value = s.promoInput,
                onValueChange = { v -> s.promoInput = v.filter { it.isLetterOrDigit() }.take(20).uppercase(); s.promoError = null },
                label = { Text(t(K.PROMO)) },
                placeholder = { Text("LUMBRE10") },
                leadingIcon = { Icon(Icons.Rounded.LocalOffer, null) },
                singleLine = true,
                isError = s.promoError != null,
                supportingText = {
                    when {
                        s.promoError != null -> Text(t(s.promoError!!))
                        s.promo != null -> Text(t(K.PROMO_OK, s.promo!!.percent), color = LocalExtras.current.ok)
                    }
                },
                keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Characters, imeAction = ImeAction.Done),
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier.weight(1f),
            )
            Spacer(Modifier.width(10.dp))
            LumbreButton(t(K.APPLY), { applyPromo(false) }, Modifier.padding(top = 6.dp), kind = BtnKind.Secondary)
        }
    }
}

@Composable
private fun StepDetails(s: BookingState) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
        FormField(s, "name", s.name, { s.name = it.take(80) }, t(K.NAME), Validation.name(s.name),
            KeyboardOptions(capitalization = KeyboardCapitalization.Words, keyboardType = KeyboardType.Text, imeAction = ImeAction.Next))
        FormField(s, "email", s.email, { s.email = it.take(254).trim() }, t(K.EMAIL), Validation.email(s.email),
            KeyboardOptions(keyboardType = KeyboardType.Email, imeAction = ImeAction.Next), placeholder = "nombre@correo.com")
        val suggestion = Validation.emailSuggestion(s.email)
        AnimatedVisibility(suggestion != null, enter = expandVertically() + fadeIn(), exit = shrinkVertically() + fadeOut()) {
            AssistChip(onClick = { suggestion?.let { s.email = it } }, label = { Text(t(K.E_EMAIL_TYPO, suggestion ?: "")) })
        }
        FormField(s, "phone", s.phone, { v -> s.phone = v.filter { it.isDigit() || it in "+ ().-" }.take(22) }, t(K.PHONE), Validation.phone(s.phone),
            KeyboardOptions(keyboardType = KeyboardType.Phone, imeAction = ImeAction.Next), supporting = t(K.PHONE_HINT), placeholder = "+52 55 1234 5678")
        OutlinedTextField(
            value = s.notes, onValueChange = { s.notes = it.take(500) }, label = { Text(t(K.NOTES)) },
            minLines = 2, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth(),
        )
        Spacer(Modifier.height(4.dp))
        val consentError = s.tried[3] == true && !s.consent
        Row(
            Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).bounceClick(scaleDown = 0.99f) { s.consent = !s.consent }.padding(vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Checkbox(checked = s.consent, onCheckedChange = { s.consent = it })
            Text(t(K.CONSENT), style = MaterialTheme.typography.bodyMedium, color = if (consentError) MaterialTheme.colorScheme.error else Color.Unspecified)
        }
        AnimatedVisibility(consentError) { Text(t(K.E_CONSENT), color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall) }
        s.formError?.let { Text(t(it), color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyMedium) }
    }
}

@Composable
private fun FormField(
    s: BookingState, key: String, value: String, onChange: (String) -> Unit, label: String, error: K?,
    keyboard: KeyboardOptions, supporting: String? = null, placeholder: String? = null,
) {
    var hadFocus by remember { mutableStateOf(false) }
    val show = s.show(3, key) && error != null
    OutlinedTextField(
        value = value, onValueChange = onChange,
        label = { Text(label) },
        placeholder = placeholder?.let { { Text(it) } },
        singleLine = true,
        isError = show,
        trailingIcon = if (error == null && value.isNotBlank()) ({ Icon(Icons.Rounded.Check, null, tint = LocalExtras.current.ok) }) else null,
        supportingText = when {
            show -> ({ Text(t(error!!)) })
            supporting != null -> ({ Text(supporting) })
            else -> null
        },
        keyboardOptions = keyboard,
        shape = RoundedCornerShape(16.dp),
        modifier = Modifier.fillMaxWidth().onFocusChanged {
            if (it.isFocused) hadFocus = true else if (hadFocus && value.isNotEmpty()) s.touched[key] = true
        },
    )
}

@Composable
private fun QuoteSummary(quote: Quote?, room: RoomId, expanded: Boolean) {
    var open by remember { mutableStateOf(expanded) }
    Column {
        if (expanded) {
            Text(t(K.SUMMARY), style = MaterialTheme.typography.headlineSmall)
            Spacer(Modifier.height(16.dp))
        }
        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
            Column(Modifier.weight(1f)) {
                Text(t(K.TOTAL), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                if (quote != null) AnimatedMoney(quote.totalEur, MaterialTheme.typography.headlineMedium, MaterialTheme.colorScheme.primary)
                else Text("—", style = MaterialTheme.typography.headlineMedium)
            }
            if (!expanded && quote != null) {
                Row(
                    Modifier.clip(RoundedCornerShape(50)).bounceClick { open = !open }.padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text(t(K.BREAKDOWN), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                    Icon(if (open) Icons.Rounded.ExpandMore else Icons.Rounded.ExpandLess, null, tint = MaterialTheme.colorScheme.primary)
                }
            }
        }
        AnimatedVisibility(open && quote != null, enter = expandVertically(spring(dampingRatio = 0.8f)) + fadeIn(), exit = shrinkVertically() + fadeOut()) {
            if (quote != null) Column(Modifier.padding(top = 12.dp)) {
                quote.lines.forEach { line -> SummaryLine(line, quote, room) }
                HorizontalDivider(Modifier.padding(vertical = 10.dp), color = MaterialTheme.colorScheme.outlineVariant)
                Text(t(K.PER_NIGHT_AVG, money(quote.perNightEur)), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(t(K.TAXES_INCLUDED), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun SummaryLine(line: QuoteLine, quote: Quote, room: RoomId) {
    val lang = LocalLang.current
    val label = when (line.kind) {
        LineKind.ROOM -> "${t(Catalog.room(room).name)} × ${nights(lang, quote.nights)}"
        LineKind.WEEKEND -> t(K.LINE_WEEKEND)
        LineKind.EXTRA -> t(Catalog.extraName(line.extra!!))
        LineKind.LONG_STAY -> t(K.LINE_LONGSTAY, line.percent)
        LineKind.PROMO -> t(K.LINE_PROMO, line.percent)
        LineKind.TAX -> t(K.LINE_TAX, line.percent)
    }
    Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        Text(label, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
        Text(
            (if (line.isDiscount) "−" else "") + money(kotlin.math.abs(line.amountEur)),
            style = MaterialTheme.typography.bodyMedium,
            color = if (line.isDiscount) LocalExtras.current.ok else MaterialTheme.colorScheme.onSurface,
        )
    }
}

@Composable
private fun SuccessView(res: Reservation, quote: Quote?, onTrips: () -> Unit, onHome: () -> Unit) {
    val lang = LocalLang.current
    val check = remember { Animatable(0f) }
    LaunchedEffect(Unit) { delay(150); check.animateTo(1f, spring(dampingRatio = 0.45f, stiffness = 260f)) }
    Box(Modifier.fillMaxSize()) {
        MaxWidth(Modifier.align(Alignment.Center), max = 520.dp) {
            Column(
                Modifier.fillMaxWidth().statusBarsPadding().padding(28.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Box(
                    Modifier.size(104.dp).graphicsLayer { scaleX = check.value; scaleY = check.value }
                        .clip(CircleShape).background(LocalExtras.current.ok),
                    contentAlignment = Alignment.Center,
                ) { Icon(Icons.Rounded.Check, null, tint = Color.White, modifier = Modifier.size(60.dp)) }
                Spacer(Modifier.height(24.dp))
                LumiSays(t(K.L_OK), Mood.Party)
                Spacer(Modifier.height(20.dp))
                Text(t(K.OK_TITLE), style = MaterialTheme.typography.displaySmall, textAlign = TextAlign.Center, modifier = Modifier.appear(1))
                Spacer(Modifier.height(10.dp))
                Text(
                    t(K.OK_TEXT, res.guestName.substringBefore(' '), nights(lang, res.checkIn.daysUntil(res.checkOut)), t(Catalog.room(res.room).name)),
                    style = MaterialTheme.typography.bodyLarge, textAlign = TextAlign.Center,
                    color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.appear(2),
                )
                Spacer(Modifier.height(20.dp))
                Row(
                    Modifier.appear(3).clip(RoundedCornerShape(50)).background(MaterialTheme.colorScheme.surfaceContainer).padding(horizontal = 20.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("${t(K.REF)}  ", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(res.ref, style = MaterialTheme.typography.titleMedium, fontFamily = FontFamily.Monospace)
                    Text("  ·  ${money(res.totalEur)}", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                }
                Spacer(Modifier.height(28.dp))
                LumbreButton(t(K.GO_TRIPS), onTrips, Modifier.fillMaxWidth())
                Spacer(Modifier.height(10.dp))
                LumbreButton(t(K.GO_HOME), onHome, Modifier.fillMaxWidth(), kind = BtnKind.Secondary)
            }
        }
        ConfettiBurst(res.ref)
    }
}
