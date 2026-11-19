package com.lumbre.hotel.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AdminPanelSettings
import androidx.compose.material.icons.rounded.Bed
import androidx.compose.material.icons.rounded.DeleteOutline
import androidx.compose.material.icons.rounded.EventAvailable
import androidx.compose.material.icons.rounded.Laptop
import androidx.compose.material.icons.rounded.Logout
import androidx.compose.material.icons.rounded.MoreVert
import androidx.compose.material.icons.rounded.Paid
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material.icons.rounded.TrendingUp
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.FilterChip
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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.PromoCode
import com.lumbre.hotel.data.Reservation
import com.lumbre.hotel.data.ReservationStatus
import com.lumbre.hotel.data.RoomConfig
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.data.today
import com.lumbre.hotel.domain.Format
import com.lumbre.hotel.domain.Validation
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.i18n.tr
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.LocalSnackbar
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.Lumi
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.Mood
import com.lumbre.hotel.ui.components.StatusChip
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.money
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlinx.coroutines.launch
import org.jetbrains.compose.resources.painterResource

/** Panel administrativo. Solo se construye en la web y con sesión de administrador. */
@Composable
fun AdminScreen(onGoProfile: () -> Unit) {
    val repo = AppGraph.repo
    val prefs by repo.prefs.collectAsState()

    if (!Capabilities.adminPanel) {
        Notice(Icons.Rounded.Laptop, t(K.ADMIN_WEB_ONLY_SUB), t(K.ADMIN_WEB_ONLY_TEXT)) {}
        return
    }
    val role by repo.role.collectAsState()
    if (!Capabilities.admin(role)) {
        Notice(Icons.Rounded.AdminPanelSettings, t(K.AD_GUARD_TITLE), if (repo.cloud) t(K.REC_GUARD) else t(K.AD_GUARD_SUB)) {
            if (!repo.cloud) LumbreButton(t(K.AD_ENTER), { repo.setAdmin(true) }, icon = Icons.Rounded.AdminPanelSettings)
        }
        return
    }
    val catalog = Capabilities.manageCatalog(role)

    val reservations by repo.reservations.collectAsState()
    val rooms by repo.rooms.collectAsState()
    val promos by repo.promos.collectAsState()
    var tab by remember { mutableIntStateOf(0) }

    MaxWidth(Modifier.fillMaxSize(), max = 1240.dp) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).statusBarsPadding().padding(24.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.appear(0)) {
                Column(Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(t(K.AD_TITLE), style = MaterialTheme.typography.displaySmall)
                        Spacer(Modifier.width(12.dp))
                        Badge(t(K.DEMO))
                    }
                    Text(t(K.AD_SUB), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                if (!repo.cloud) TextButton(onClick = { repo.setAdmin(false); onGoProfile() }) {
                    Icon(Icons.Rounded.Logout, null); Spacer(Modifier.width(6.dp)); Text(t(K.AD_EXIT))
                }
            }
            Spacer(Modifier.height(24.dp))
            Kpis(reservations, Modifier.appear(1))
            Spacer(Modifier.height(16.dp))
            RevenueChart(reservations, Modifier.appear(2))
            Spacer(Modifier.height(24.dp))
            PrimaryTabRow(selectedTabIndex = tab, containerColor = MaterialTheme.colorScheme.background) {
                (if (catalog) listOf(K.AD_TAB_RES, K.AD_TAB_ROOMS, K.AD_TAB_PROMOS) else listOf(K.AD_TAB_RES)).forEachIndexed { i, k ->
                    Tab(selected = tab == i, onClick = { tab = i }, text = { Text(t(k)) })
                }
            }
            Spacer(Modifier.height(16.dp))
            AnimatedContent(tab, transitionSpec = { fadeIn(tween(220)) togetherWith fadeOut(tween(120)) }, label = "tab") { current ->
                when (current) {
                    0 -> ReservationsTab(reservations)
                    1 -> RoomsTab(rooms)
                    else -> PromosTab(promos)
                }
            }
        }
    }
}

@Composable
private fun Notice(icon: ImageVector, title: String, text: String, action: @Composable () -> Unit) {
    Box(Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
        Column(Modifier.widthIn(max = 460.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Lumi(Mood.Think, Unit, Modifier.size(110.dp).appear())
            Spacer(Modifier.height(12.dp))
            Icon(icon, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))
            Spacer(Modifier.height(8.dp))
            Text(title, style = MaterialTheme.typography.headlineSmall, textAlign = TextAlign.Center)
            Spacer(Modifier.height(8.dp))
            Text(text, style = MaterialTheme.typography.bodyLarge, textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Spacer(Modifier.height(20.dp))
            action()
        }
    }
}

@Composable
private fun Kpis(reservations: List<Reservation>, modifier: Modifier) {
    val today = remember { today() }
    val valid = reservations.filter { it.status != ReservationStatus.CANCELLED }
    val active = valid.count { it.checkOut >= today }
    val revenue = valid.sumOf { it.totalEur }
    val occupied = valid.count { it.checkIn <= today && today < it.checkOut }
    val avg = if (valid.isEmpty()) 0.0 else revenue / valid.size
    FlowRow(modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp), maxItemsInEachRow = 4) {
        Kpi(Icons.Rounded.EventAvailable, t(K.KPI_ACTIVE), active.toString(), Modifier.weight(1f))
        Kpi(Icons.Rounded.Paid, t(K.KPI_REVENUE), money(revenue), Modifier.weight(1f))
        Kpi(Icons.Rounded.Bed, t(K.KPI_OCC), "$occupied / 86", Modifier.weight(1f))
        Kpi(Icons.Rounded.TrendingUp, t(K.KPI_AVG), money(avg), Modifier.weight(1f))
    }
}

@Composable
private fun Kpi(icon: ImageVector, label: String, value: String, modifier: Modifier) {
    Card(
        modifier.widthIn(min = 200.dp), shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
    ) {
        Column(Modifier.padding(20.dp)) {
            Icon(icon, null, tint = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.height(10.dp))
            AnimatedContent(value, transitionSpec = { fadeIn() togetherWith fadeOut() }, label = "kpi") {
                Text(it, style = MaterialTheme.typography.headlineMedium)
            }
            Text(label, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun RevenueChart(reservations: List<Reservation>, modifier: Modifier) {
    val byRoom = RoomId.entries.associateWith { id ->
        reservations.filter { it.room == id && it.status != ReservationStatus.CANCELLED }.sumOf { it.totalEur }
    }
    val max = (byRoom.values.maxOrNull() ?: 0.0).coerceAtLeast(1.0)
    val grow = remember { Animatable(0f) }
    LaunchedEffect(byRoom) { grow.snapTo(0f); grow.animateTo(1f, spring(dampingRatio = 0.7f, stiffness = 90f)) }
    val primary = MaterialTheme.colorScheme.primary
    val gold = LocalExtras.current.gold
    val track = MaterialTheme.colorScheme.surfaceContainerHigh
    Card(
        modifier.fillMaxWidth(), shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
    ) {
        Column(Modifier.padding(20.dp)) {
            Text(t(K.AD_REV_BY_ROOM), style = MaterialTheme.typography.titleLarge)
            Spacer(Modifier.height(16.dp))
            RoomId.entries.forEachIndexed { i, id ->
                val value = byRoom.getValue(id)
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 6.dp)) {
                    Text(t(Catalog.room(id).name), style = MaterialTheme.typography.bodyMedium, modifier = Modifier.width(150.dp), maxLines = 1, overflow = TextOverflow.Ellipsis)
                    Canvas(Modifier.weight(1f).height(18.dp)) {
                        val r = CornerRadius(size.height / 2)
                        drawRoundRect(track, cornerRadius = r)
                        drawRoundRect(if (i % 2 == 0) primary else gold, size = Size(size.width * (value / max).toFloat() * grow.value, size.height), cornerRadius = r, topLeft = Offset.Zero)
                    }
                    Text(money(value), style = MaterialTheme.typography.labelLarge, modifier = Modifier.width(120.dp), textAlign = TextAlign.End)
                }
            }
        }
    }
}

@Composable
private fun ReservationsTab(reservations: List<Reservation>) {
    val repo = AppGraph.repo
    val lang = LocalLang.current
    var query by remember { mutableStateOf("") }
    var filter by remember { mutableStateOf<ReservationStatus?>(null) }
    val shown = reservations
        .filter { filter == null || it.status == filter }
        .filter { query.isBlank() || it.guestName.contains(query, true) || it.ref.contains(query, true) || it.email.contains(query, true) }
        .sortedBy { it.checkIn }

    Column {
        OutlinedTextField(
            query, { query = it.take(60) }, leadingIcon = { Icon(Icons.Rounded.Search, null) },
            placeholder = { Text(t(K.SEARCH)) }, singleLine = true, shape = RoundedCornerShape(50), modifier = Modifier.fillMaxWidth(),
        )
        Spacer(Modifier.height(12.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            FilterChip(filter == null, { filter = null }, label = { Text(t(K.ALL)) })
            ReservationStatus.entries.forEach { st -> FilterChip(filter == st, { filter = st }, label = { Text(t(Catalog.status(st))) }) }
        }
        Spacer(Modifier.height(12.dp))
        Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
            BoxWithConstraints {
                val compact = maxWidth < 760.dp
                Column(Modifier.padding(vertical = 8.dp)) {
                    if (!compact) {
                        Row(Modifier.padding(horizontal = 20.dp, vertical = 10.dp)) {
                            listOf(K.AD_GUEST to 2.2f, K.AD_ROOM to 1.6f, K.AD_DATES to 1.6f, K.AD_TOTAL to 1f, K.AD_STATUS to 1.2f).forEach { (k, w) ->
                                Text(t(k), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(w))
                            }
                            Spacer(Modifier.width(48.dp))
                        }
                        HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
                    }
                    if (shown.isEmpty()) Text(t(K.AD_NO_RESULTS), Modifier.padding(24.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
                    shown.forEachIndexed { i, r ->
                        if (i > 0) HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f))
                        val actions: @Composable () -> Unit = { RowActions(r) { st -> repo.setStatus(r.ref, st) } }
                        if (compact) {
                            Row(Modifier.padding(horizontal = 16.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
                                Column(Modifier.weight(1f)) {
                                    Text(r.guestName, style = MaterialTheme.typography.titleSmall)
                                    Text("${t(Catalog.room(r.room).name)} · ${Format.range(r.checkIn, r.checkOut, lang)}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    Spacer(Modifier.height(6.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) { StatusChip(r.status); Spacer(Modifier.width(10.dp)); Text(money(r.totalEur), style = MaterialTheme.typography.labelLarge) }
                                }
                                actions()
                            }
                        } else {
                            Row(Modifier.padding(horizontal = 20.dp, vertical = 12.dp), verticalAlignment = Alignment.CenterVertically) {
                                Column(Modifier.weight(2.2f)) {
                                    Text(r.guestName + if (r.mine) " ★" else "", style = MaterialTheme.typography.titleSmall)
                                    Text(r.ref, style = MaterialTheme.typography.bodySmall, fontFamily = FontFamily.Monospace, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                                Text(t(Catalog.room(r.room).name), style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1.6f))
                                Text(Format.range(r.checkIn, r.checkOut, lang), style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1.6f))
                                Text(money(r.totalEur), style = MaterialTheme.typography.titleSmall, modifier = Modifier.weight(1f))
                                Box(Modifier.weight(1.2f)) { StatusChip(r.status) }
                                actions()
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun RowActions(r: Reservation, onStatus: (ReservationStatus) -> Unit) {
    var open by remember { mutableStateOf(false) }
    Box {
        IconButton(onClick = { open = true }) { Icon(Icons.Rounded.MoreVert, t(K.AD_STATUS)) }
        DropdownMenu(expanded = open, onDismissRequest = { open = false }) {
            if (r.status != ReservationStatus.CONFIRMED) DropdownMenuItem(text = { Text(t(K.ACT_CONFIRM)) }, onClick = { onStatus(ReservationStatus.CONFIRMED); open = false })
            if (r.status != ReservationStatus.CHECKED_IN) DropdownMenuItem(text = { Text(t(K.ACT_CHECKIN)) }, onClick = { onStatus(ReservationStatus.CHECKED_IN); open = false })
            if (r.status != ReservationStatus.CANCELLED) DropdownMenuItem(
                text = { Text(t(K.ACT_CANCEL), color = MaterialTheme.colorScheme.error) },
                onClick = { onStatus(ReservationStatus.CANCELLED); open = false },
            )
        }
    }
}

@Composable
private fun RoomsTab(rooms: List<RoomConfig>) {
    BoxWithConstraints {
        if (maxWidth >= 900.dp) {
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                rooms.forEach { cfg -> RoomEditor(cfg, Modifier.weight(1f)) }
            }
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                rooms.forEach { cfg -> RoomEditor(cfg, Modifier.fillMaxWidth()) }
            }
        }
    }
}

@Composable
private fun RoomEditor(cfg: RoomConfig, modifier: Modifier) {
    val repo = AppGraph.repo
    val info = Catalog.room(cfg.id)
    val snackbar = LocalSnackbar.current
    val scope = rememberCoroutineScope()
    val lang = LocalLang.current
    var price by remember(cfg) { mutableStateOf(cfg.nightlyEur.toString()) }
    var available by remember(cfg) { mutableStateOf(cfg.available) }
    val priceInt = price.toIntOrNull()
    val priceError = priceInt == null || priceInt !in 30..5000
    val dirty = priceInt != cfg.nightlyEur || available != cfg.available

    Card(modifier, shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
        Image(painterResource(info.image), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxWidth().height(120.dp))
        Column(Modifier.padding(20.dp)) {
            Text(t(info.name), style = MaterialTheme.typography.titleLarge)
            Spacer(Modifier.height(12.dp))
            OutlinedTextField(
                price, { v -> price = v.filter { it.isDigit() }.take(4) }, label = { Text(t(K.AD_PRICE)) },
                isError = priceError, supportingText = { if (priceError) Text(t(K.E_PRICE)) else Text(money(priceInt?.toDouble() ?: 0.0)) },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number), singleLine = true,
                shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth(),
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(t(K.AD_AVAILABLE), style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
                Switch(available, { available = it })
            }
            Spacer(Modifier.height(8.dp))
            LumbreButton(
                t(K.SAVE), enabled = dirty && !priceError, modifier = Modifier.fillMaxWidth(),
                onClick = {
                    repo.updateRoom(cfg.id, priceInt ?: cfg.nightlyEur, available)
                    scope.launch { snackbar.showSnackbar(tr(lang, K.AD_SAVED)) }
                },
            )
        }
    }
}

@Composable
private fun PromosTab(promos: List<PromoCode>) {
    val repo = AppGraph.repo
    var code by remember { mutableStateOf("") }
    var percent by remember { mutableStateOf("10") }
    var tried by remember { mutableStateOf(false) }
    val codeError = Validation.promoCode(code)
    val pct = percent.toIntOrNull()
    val pctError = pct == null || pct !in 5..50

    Row(horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.Top) {
        Card(Modifier.weight(1.4f), shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
            Column(Modifier.padding(vertical = 8.dp)) {
                promos.sortedBy { it.code }.forEachIndexed { i, p ->
                    if (i > 0) HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.6f))
                    Row(Modifier.padding(horizontal = 20.dp, vertical = 10.dp), verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text(p.code, style = MaterialTheme.typography.titleMedium, fontFamily = FontFamily.Monospace)
                            Text("−${p.percent} %", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Text(if (p.active) t(K.AD_ACTIVE) else "", style = MaterialTheme.typography.labelMedium, color = LocalExtras.current.ok)
                        Spacer(Modifier.width(8.dp))
                        Switch(p.active, { repo.upsertPromo(p.copy(active = it)) })
                        IconButton(onClick = { repo.deletePromo(p.code) }) { Icon(Icons.Rounded.DeleteOutline, t(K.DELETE), tint = MaterialTheme.colorScheme.error) }
                    }
                }
            }
        }
        Card(Modifier.weight(1f), shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
            Column(Modifier.padding(20.dp)) {
                Text(t(K.AD_NEW_PROMO), style = MaterialTheme.typography.titleLarge)
                Spacer(Modifier.height(12.dp))
                OutlinedTextField(
                    code, { v -> code = v.filter { it.isLetterOrDigit() }.uppercase().take(20) }, label = { Text(t(K.AD_CODE)) },
                    isError = tried && codeError != null, supportingText = { if (tried && codeError != null) Text(t(codeError)) },
                    singleLine = true, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth(),
                )
                OutlinedTextField(
                    percent, { v -> percent = v.filter { it.isDigit() }.take(2) }, label = { Text(t(K.AD_PERCENT)) },
                    isError = tried && pctError, supportingText = { if (tried && pctError) Text(t(K.E_PERCENT)) },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    singleLine = true, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth(),
                )
                Spacer(Modifier.height(8.dp))
                LumbreButton(t(K.ADD), kind = BtnKind.Gold, modifier = Modifier.fillMaxWidth(), onClick = {
                    tried = true
                    if (codeError == null && !pctError) {
                        repo.upsertPromo(PromoCode(code, pct!!, active = true)); code = ""; percent = "10"; tried = false
                    }
                })
            }
        }
    }
}
