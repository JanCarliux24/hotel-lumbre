package com.lumbre.hotel.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowDropDown
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material.icons.rounded.VerifiedUser
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.PrimaryTabRow
import androidx.compose.material3.Switch
import androidx.compose.material3.Tab
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.Account
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.Params
import com.lumbre.hotel.data.Role
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.i18n.tr
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.LocalSnackbar
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlinx.coroutines.launch
import kotlinx.datetime.TimeZone
import kotlinx.datetime.toLocalDateTime
import kotlin.time.Instant

fun roleKey(r: Role) = when (r) {
    Role.GUEST -> K.ROLE_GUEST; Role.STAFF -> K.ROLE_STAFF; Role.ADMIN -> K.ROLE_ADMIN; Role.SUPERADMIN -> K.ROLE_SUPERADMIN
}

/** Panel exclusivo del superusuario y solo en la web. */
@Composable
fun SuperAdminScreen() {
    val repo = AppGraph.repo
    val role by repo.role.collectAsState()
    val scope = rememberCoroutineScope()
    if (!Capabilities.superPanel(role)) { GuardNotice(t(K.SU_GUARD)); return }
    var tab by remember { mutableIntStateOf(0) }

    MaxWidth(Modifier.fillMaxSize(), max = 1240.dp) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).statusBarsPadding().padding(24.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.appear()) {
                Column(Modifier.weight(1f)) {
                    Text(t(K.SU_TITLE), style = MaterialTheme.typography.displaySmall)
                    Text(t(K.SU_SUB), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                TextButton(onClick = { scope.launch { repo.refreshAll() } }) { Icon(Icons.Rounded.Refresh, null); Spacer(Modifier.width(6.dp)); Text(t(K.SU_REFRESH)) }
            }
            Spacer(Modifier.height(20.dp))
            PrimaryTabRow(selectedTabIndex = tab, containerColor = MaterialTheme.colorScheme.background) {
                listOf(K.SU_USERS, K.SU_PARAMS, K.SU_AUDIT, K.SU_SECURITY).forEachIndexed { i, k ->
                    Tab(selected = tab == i, onClick = { tab = i }, text = { Text(t(k)) })
                }
            }
            Spacer(Modifier.height(16.dp))
            AnimatedContent(tab, transitionSpec = { fadeIn(tween(200)) togetherWith fadeOut(tween(120)) }, label = "su") {
                when (it) {
                    0 -> UsersTab()
                    1 -> ParamsTab()
                    2 -> AuditTab()
                    else -> SecurityTab()
                }
            }
        }
    }
}

@Composable
private fun UsersTab() {
    val repo = AppGraph.repo
    val users by repo.users.collectAsState()
    val me by repo.account.collectAsState()
    var query by remember { mutableStateOf("") }
    val shown = users.filter { query.isBlank() || it.email.contains(query, true) || it.name.contains(query, true) }
    Column {
        OutlinedTextField(query, { query = it.take(60) }, leadingIcon = { Icon(Icons.Rounded.Search, null) },
            placeholder = { Text(t(K.SEARCH)) }, singleLine = true, shape = RoundedCornerShape(50), modifier = Modifier.fillMaxWidth())
        Spacer(Modifier.height(12.dp))
        Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
            Column(Modifier.padding(vertical = 8.dp)) {
                if (shown.isEmpty()) Text(t(K.AD_NO_RESULTS), Modifier.padding(20.dp))
                shown.forEachIndexed { i, u ->
                    if (i > 0) HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    UserRow(u, isMe = u.uid == me?.uid)
                }
            }
        }
    }
}

@Composable
private fun UserRow(u: Account, isMe: Boolean) {
    val repo = AppGraph.repo
    var open by remember { mutableStateOf(false) }
    Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
        Column(Modifier.weight(1f)) {
            Text(u.name.ifBlank { u.email } + if (isMe) " · ${t(K.SU_YOU)}" else "", style = MaterialTheme.typography.titleSmall)
            Text(u.email, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            if (u.disabled) Text(t(K.SU_BLOCKED), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.error)
        }
        Box {
            TextButton(onClick = { open = true }, enabled = !isMe) { Text(t(roleKey(u.role))); Icon(Icons.Rounded.ArrowDropDown, null) }
            DropdownMenu(open, { open = false }) {
                Role.entries.forEach { r ->
                    DropdownMenuItem(text = { Text(t(roleKey(r))) }, onClick = { repo.setUserRole(u.uid, r); open = false })
                }
            }
        }
        if (!isMe) TextButton(onClick = { repo.setUserDisabled(u.uid, !u.disabled) }) {
            Text(if (u.disabled) t(K.SU_UNBLOCK) else t(K.SU_BLOCK), color = if (u.disabled) LocalExtras.current.ok else MaterialTheme.colorScheme.error)
        }
    }
}

/** Campo numérico con validación de rango. */
@Composable
private fun NumField(label: K, value: String, range: IntRange, onChange: (String) -> Unit, modifier: Modifier = Modifier): Boolean {
    val n = value.toIntOrNull()
    val ok = n != null && n in range
    OutlinedTextField(
        value, { v -> onChange(v.filter { it.isDigit() }.take(4)) }, label = { Text(t(label)) },
        isError = !ok, supportingText = { if (!ok) Text(t(K.E_RANGE, range.first, range.last)) },
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), singleLine = true,
        shape = RoundedCornerShape(16.dp), modifier = modifier,
    )
    return ok
}

@Composable
private fun ParamsTab() {
    val repo = AppGraph.repo
    val current by repo.params.collectAsState()
    val snackbar = LocalSnackbar.current
    val scope = rememberCoroutineScope()
    val lang = LocalLang.current
    val fields = remember(current) {
        mutableMapOf(
            K.SU_P_TAX to mutableStateOf(current.taxPercent.toString()),
            K.SU_P_WEEKEND to mutableStateOf(current.weekendSurchargePercent.toString()),
            K.SU_P_LONGDISC to mutableStateOf(current.longStayDiscountPercent.toString()),
            K.SU_P_LONGNIGHTS to mutableStateOf(current.longStayNights.toString()),
            K.SU_P_MAXNIGHTS to mutableStateOf(current.maxNights.toString()),
            K.SU_P_MONTHS to mutableStateOf(current.maxMonthsAhead.toString()),
            K.SU_P_COOLDOWN to mutableStateOf(current.bookingCooldownSec.toString()),
            K.SU_P_ATTEMPTS to mutableStateOf(current.maxLoginAttempts.toString()),
            K.SU_P_LOCKOUT to mutableStateOf(current.lockoutSec.toString()),
            K.SU_P_MINPASS to mutableStateOf(current.minPasswordLength.toString()),
        )
    }
    val ranges = mapOf(
        K.SU_P_TAX to 0..30, K.SU_P_WEEKEND to 0..50, K.SU_P_LONGDISC to 0..50, K.SU_P_LONGNIGHTS to 2..30,
        K.SU_P_MAXNIGHTS to 1..90, K.SU_P_MONTHS to 1..24, K.SU_P_COOLDOWN to 0..600, K.SU_P_ATTEMPTS to 3..10,
        K.SU_P_LOCKOUT to 30..3600, K.SU_P_MINPASS to 8..64,
    )
    var maintenance by remember(current) { mutableStateOf(current.maintenance) }
    var message by remember(current) { mutableStateOf(current.maintenanceMessage) }

    Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
        Column(Modifier.padding(20.dp)) {
            var allOk = true
            BoxWithConstraints {
                val cols = if (maxWidth > 700.dp) 2 else 1
                Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    fields.keys.toList().chunked(cols).forEach { row ->
                        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                            row.forEach { k ->
                                val st = fields.getValue(k)
                                val ok = NumField(k, st.value, ranges.getValue(k), { st.value = it }, Modifier.weight(1f))
                                if (!ok) allOk = false
                            }
                            if (row.size < cols) Spacer(Modifier.weight(1f))
                        }
                    }
                }
            }
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(top = 8.dp)) {
                Text(t(K.SU_P_MAINT), style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                Switch(maintenance, { maintenance = it })
            }
            if (maintenance) OutlinedTextField(message, { message = it.take(160) }, label = { Text(t(K.SU_P_MAINT_MSG)) }, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth())
            Spacer(Modifier.height(14.dp))
            LumbreButton(t(K.SAVE), enabled = allOk, kind = BtnKind.Gold, onClick = {
                fun v(k: K) = fields.getValue(k).value.toInt()
                repo.setParams(
                    Params(
                        taxPercent = v(K.SU_P_TAX), weekendSurchargePercent = v(K.SU_P_WEEKEND),
                        longStayDiscountPercent = v(K.SU_P_LONGDISC), longStayNights = v(K.SU_P_LONGNIGHTS),
                        maxNights = v(K.SU_P_MAXNIGHTS), maxMonthsAhead = v(K.SU_P_MONTHS), bookingCooldownSec = v(K.SU_P_COOLDOWN),
                        maxLoginAttempts = v(K.SU_P_ATTEMPTS), lockoutSec = v(K.SU_P_LOCKOUT), minPasswordLength = v(K.SU_P_MINPASS),
                        maintenance = maintenance, maintenanceMessage = message.trim(),
                    )
                )
                scope.launch { snackbar.showSnackbar(tr(lang, K.AD_SAVED)) }
            })
        }
    }
}

@Composable
private fun AuditTab() {
    val repo = AppGraph.repo
    val audit by repo.audit.collectAsState()
    Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
        Column(Modifier.padding(vertical = 8.dp)) {
            if (audit.isEmpty()) Text(t(K.SU_EMPTY), Modifier.padding(20.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
            audit.forEachIndexed { i, e ->
                if (i > 0) HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                val dt = Instant.fromEpochMilliseconds(e.at).toLocalDateTime(TimeZone.currentSystemDefault())
                Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 10.dp)) {
                    Text("${dt.date} ${dt.hour.toString().padStart(2, '0')}:${dt.minute.toString().padStart(2, '0')}",
                        fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodySmall, modifier = Modifier.width(140.dp))
                    Text(e.action, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, modifier = Modifier.width(140.dp))
                    Column(Modifier.weight(1f)) {
                        Text(e.target, style = MaterialTheme.typography.bodyMedium)
                        Text(e.actor, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
private fun SecurityTab() {
    Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
        Column(Modifier.padding(20.dp)) {
            listOf(K.SU_SEC_1, K.SU_SEC_2, K.SU_SEC_3, K.SU_SEC_4, K.SU_SEC_5, K.SU_SEC_6).forEachIndexed { i, k ->
                Row(Modifier.padding(vertical = 8.dp).appear(i), verticalAlignment = Alignment.Top) {
                    Icon(Icons.Rounded.VerifiedUser, null, tint = LocalExtras.current.ok, modifier = Modifier.size(22.dp))
                    Spacer(Modifier.width(12.dp))
                    Text(t(k), style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}

@Suppress("unused") private val keepIconButton: @Composable () -> Unit = { IconButton(onClick = {}) {} }
