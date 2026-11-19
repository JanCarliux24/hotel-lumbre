package com.lumbre.hotel.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.FlightLand
import androidx.compose.material.icons.rounded.FlightTakeoff
import androidx.compose.material.icons.rounded.Hotel
import androidx.compose.material.icons.rounded.Login
import androidx.compose.material.icons.rounded.Refresh
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.Reservation
import com.lumbre.hotel.data.ReservationStatus
import com.lumbre.hotel.data.today
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.StatusChip
import com.lumbre.hotel.ui.components.appear
import kotlinx.coroutines.launch

/** Recepción: disponible en móvil y web para el personal (rol STAFF o superior). */
@Composable
fun ReceptionScreen() {
    val repo = AppGraph.repo
    val role by repo.role.collectAsState()
    val all by repo.reservations.collectAsState()
    val scope = rememberCoroutineScope()
    val today = remember { today() }

    if (!Capabilities.reception(role)) {
        GuardNotice(t(K.REC_GUARD))
        return
    }
    val valid = all.filter { it.status != ReservationStatus.CANCELLED }
    val arrivals = valid.filter { it.checkIn == today && it.status == ReservationStatus.CONFIRMED }
    val inHouse = valid.filter { it.status == ReservationStatus.CHECKED_IN && it.checkOut > today }
    val departures = valid.filter { it.checkOut == today }

    MaxWidth(Modifier.fillMaxSize(), max = 900.dp) {
        LazyColumn(Modifier.fillMaxSize(), contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            item {
                Row(Modifier.statusBarsPadding().padding(top = 8.dp).appear(), verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text(t(K.REC_TITLE), style = MaterialTheme.typography.displaySmall)
                        Text(t(K.REC_SUB), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    IconButton(onClick = { scope.launch { repo.refreshAll() } }) { Icon(Icons.Rounded.Refresh, t(K.SU_REFRESH)) }
                }
                if (Capabilities.isMobile) Text(t(K.REC_MOBILE_HINT), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
            }
            section(K.REC_ARRIVALS, Icons.Rounded.FlightLand, arrivals) { r ->
                LumbreButton(t(K.ACT_CHECKIN), { repo.setStatus(r.ref, ReservationStatus.CHECKED_IN) }, icon = Icons.Rounded.Login, height = 44.dp)
            }
            section(K.REC_INHOUSE, Icons.Rounded.Hotel, inHouse) { null }
            section(K.REC_DEPARTURES, Icons.Rounded.FlightTakeoff, departures) { r ->
                if (r.status == ReservationStatus.CONFIRMED)
                    LumbreButton(t(K.ACT_CHECKIN), { repo.setStatus(r.ref, ReservationStatus.CHECKED_IN) }, kind = BtnKind.Secondary, height = 44.dp)
            }
        }
    }
}

private fun androidx.compose.foundation.lazy.LazyListScope.section(
    title: K, icon: ImageVector, list: List<Reservation>, action: @Composable (Reservation) -> Unit?,
) {
    item {
        Row(Modifier.padding(top = 12.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(icon, null, tint = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.width(10.dp))
            Text("${t(title)} · ${list.size}", style = MaterialTheme.typography.titleLarge)
        }
    }
    if (list.isEmpty()) item { Text(t(K.REC_EMPTY), color = MaterialTheme.colorScheme.onSurfaceVariant) }
    items(list, key = { "$title-${it.ref}" }) { r ->
        Card(shape = RoundedCornerShape(20.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
            Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text(r.guestName, style = MaterialTheme.typography.titleMedium)
                    Text("${t(Catalog.room(r.room).name)} · ${r.adults + r.children} pax", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(r.ref, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.labelMedium)
                }
                StatusChip(r.status)
                Spacer(Modifier.width(10.dp))
                action(r)
            }
        }
    }
}

@Composable
fun GuardNotice(text: String) {
    Column(Modifier.fillMaxSize().padding(32.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
        com.lumbre.hotel.ui.components.Lumi(com.lumbre.hotel.ui.components.Mood.Think, Unit, Modifier.size(110.dp))
        Spacer(Modifier.size(12.dp))
        Text(text, style = MaterialTheme.typography.titleMedium, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
    }
}
