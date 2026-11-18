package com.lumbre.hotel.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.BrightnessAuto
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.DarkMode
import androidx.compose.material.icons.rounded.LightMode
import androidx.compose.foundation.layout.size
import com.lumbre.hotel.data.ThemeMode
import androidx.compose.material3.DatePickerDialog
import androidx.compose.material3.DateRangePicker
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SelectableDates
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberDateRangePickerState
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.Currency
import com.lumbre.hotel.data.Lang
import com.lumbre.hotel.data.today
import com.lumbre.hotel.domain.Validation
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.regionName
import com.lumbre.hotel.i18n.t
import kotlinx.datetime.LocalDate
import kotlinx.datetime.TimeZone
import kotlinx.datetime.atStartOfDayIn
import kotlinx.datetime.toLocalDateTime
import kotlin.time.Instant

fun LocalDate.toUtcMillis(): Long = atStartOfDayIn(TimeZone.UTC).toEpochMilliseconds()
fun Long.utcMillisToDate(): LocalDate = Instant.fromEpochMilliseconds(this).toLocalDateTime(TimeZone.UTC).date

/** Selector de rango con límites: desde hoy hasta 18 meses vista. */
@Composable
fun DateRangeDialog(start: LocalDate?, end: LocalDate?, onDismiss: () -> Unit, onConfirm: (LocalDate, LocalDate) -> Unit) {
    val today = today()
    val last = Validation.latestBookable(today)
    val state = rememberDateRangePickerState(
        initialSelectedStartDateMillis = start?.toUtcMillis(),
        initialSelectedEndDateMillis = end?.toUtcMillis(),
        yearRange = today.year..last.year,
        selectableDates = object : SelectableDates {
            override fun isSelectableDate(utcTimeMillis: Long): Boolean = utcTimeMillis.utcMillisToDate() in today..last
            override fun isSelectableYear(year: Int): Boolean = year in today.year..last.year
        },
    )
    DatePickerDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            TextButton(
                enabled = state.selectedStartDateMillis != null && state.selectedEndDateMillis != null,
                onClick = {
                    val s = state.selectedStartDateMillis ?: return@TextButton
                    val e = state.selectedEndDateMillis ?: return@TextButton
                    onConfirm(s.utcMillisToDate(), e.utcMillisToDate())
                },
            ) { Text(t(K.APPLY)) }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text(t(K.CANCEL)) } },
    ) {
        DateRangePicker(state = state, modifier = Modifier.weight(1f), showModeToggle = false)
    }
}

/** Idioma y moneda (se guardan solos y se aplican al instante en toda la app). */
@Composable
fun PrefsSheet(onDismiss: () -> Unit) {
    val repo = AppGraph.repo
    val prefs by repo.prefs.collectAsState()
    ModalBottomSheet(onDismissRequest = onDismiss, sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 24.dp).navigationBarsPadding().padding(bottom = 24.dp)) {
            Text(t(K.PREFS_TITLE), style = MaterialTheme.typography.headlineSmall)
            Spacer(Modifier.height(20.dp))
            ThemeSelector(prefs.theme) { repo.setTheme(it) }
            Spacer(Modifier.height(20.dp))
            LanguageSelector(prefs.lang) { repo.setLang(it) }
            Spacer(Modifier.height(20.dp))
            CurrencySelector(prefs.currency) { repo.setCurrency(it) }
            Spacer(Modifier.height(16.dp))
            Text(
                regionName(prefs.region, prefs.lang)?.let { t(K.REGION, it) } ?: t(K.REGION_UNKNOWN),
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
fun ThemeSelector(selected: ThemeMode, onSelect: (ThemeMode) -> Unit) {
    val options = listOf(
        Triple(ThemeMode.LIGHT, K.THEME_LIGHT, Icons.Rounded.LightMode),
        Triple(ThemeMode.DARK, K.THEME_DARK, Icons.Rounded.DarkMode),
        Triple(ThemeMode.SYSTEM, K.THEME_SYSTEM, Icons.Rounded.BrightnessAuto),
    )
    Text(t(K.THEME), style = MaterialTheme.typography.titleSmall)
    Spacer(Modifier.height(8.dp))
    SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth()) {
        options.forEachIndexed { i, (mode, label, icon) ->
            SegmentedButton(
                selected = mode == selected,
                onClick = { onSelect(mode) },
                shape = SegmentedButtonDefaults.itemShape(i, options.size),
                icon = { Icon(icon, null, Modifier.size(18.dp)) },
            ) { Text(t(label)) }
        }
    }
}

@Composable
fun LanguageSelector(selected: Lang, onSelect: (Lang) -> Unit) {
    Text(t(K.LANGUAGE), style = MaterialTheme.typography.titleSmall)
    Spacer(Modifier.height(8.dp))
    SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth()) {
        Lang.entries.forEachIndexed { i, lang ->
            SegmentedButton(
                selected = lang == selected,
                onClick = { onSelect(lang) },
                shape = SegmentedButtonDefaults.itemShape(i, Lang.entries.size),
            ) { Text(lang.code.uppercase()) }
        }
    }
}

@Composable
fun CurrencySelector(selected: Currency, onSelect: (Currency) -> Unit) {
    Text(t(K.CURRENCY), style = MaterialTheme.typography.titleSmall)
    Spacer(Modifier.height(8.dp))
    FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Currency.entries.forEach { c ->
            FilterChip(
                selected = c == selected,
                onClick = { onSelect(c) },
                label = { Text("${c.code} ${c.symbol}") },
                leadingIcon = if (c == selected) ({ Icon(Icons.Rounded.Check, null) }) else null,
            )
        }
    }
}
