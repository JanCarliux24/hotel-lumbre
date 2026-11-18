package com.lumbre.hotel.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.BeachAccess
import androidx.compose.material.icons.rounded.Key
import androidx.compose.material.icons.rounded.Sailing
import androidx.compose.material.icons.rounded.WbSunny
import com.lumbre.hotel.ui.components.FloatingIcon
import androidx.compose.material.icons.rounded.Smartphone
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.ReservationStatus
import com.lumbre.hotel.data.today
import com.lumbre.hotel.domain.Format
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.nights
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.Lumi
import com.lumbre.hotel.ui.components.Mood
import com.lumbre.hotel.ui.components.StatusChip
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.money
import kotlinx.datetime.daysUntil
import org.jetbrains.compose.resources.painterResource

@Composable
fun TripsScreen(onBook: () -> Unit, onKey: (String) -> Unit) {
    val repo = AppGraph.repo
    val all by repo.reservations.collectAsState()
    val mine = all.filter { it.mine }.sortedByDescending { it.checkIn }
    val lang = LocalLang.current
    var cancelRef by remember { mutableStateOf<String?>(null) }
    val today = remember { today() }

    LazyVerticalGrid(
        columns = GridCells.Adaptive(380.dp),
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item(span = { GridItemSpan(maxLineSpan) }) {
            Text(t(K.TRIPS_TITLE), style = MaterialTheme.typography.displaySmall, modifier = Modifier.statusBarsPadding().padding(top = 12.dp).appear())
        }
        if (mine.isEmpty()) {
            item(span = { GridItemSpan(maxLineSpan) }) {
                Column(Modifier.fillMaxWidth().padding(top = 48.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Row(horizontalArrangement = Arrangement.spacedBy(28.dp), modifier = Modifier.appear(0)) {
                        FloatingIcon(Icons.Rounded.BeachAccess, MaterialTheme.colorScheme.tertiary, size = 30.dp)
                        FloatingIcon(Icons.Rounded.WbSunny, MaterialTheme.colorScheme.secondary, size = 34.dp, delayMs = 400)
                        FloatingIcon(Icons.Rounded.Sailing, MaterialTheme.colorScheme.primary, size = 30.dp, delayMs = 800)
                    }
                    Spacer(Modifier.height(12.dp))
                    Lumi(Mood.Think, Unit, Modifier.size(120.dp).appear(1))
                    Spacer(Modifier.height(16.dp))
                    Text(t(K.TRIPS_EMPTY), style = MaterialTheme.typography.headlineSmall, modifier = Modifier.appear(2))
                    Spacer(Modifier.height(6.dp))
                    Text(t(K.TRIPS_EMPTY_SUB), textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.appear(3))
                    Spacer(Modifier.height(24.dp))
                    LumbreButton(t(K.BOOK_NOW), onBook, Modifier.appear(4))
                }
            }
        }
        itemsIndexed(mine, key = { _, r -> r.ref }) { i, r ->
            val info = Catalog.room(r.room)
            val active = r.status != ReservationStatus.CANCELLED && r.checkOut >= today
            Card(
                Modifier.appear(i).graphicsLayer { alpha = if (r.status == ReservationStatus.CANCELLED) 0.6f else 1f },
                shape = RoundedCornerShape(28.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
                elevation = CardDefaults.cardElevation(2.dp),
            ) {
                Box {
                    Image(painterResource(info.image), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxWidth().height(150.dp))
                    Box(Modifier.padding(12.dp)) { StatusChip(r.status) }
                }
                Column(Modifier.padding(20.dp)) {
                    Text(t(info.name), style = MaterialTheme.typography.headlineSmall)
                    Spacer(Modifier.height(4.dp))
                    Text(
                        "${Format.range(r.checkIn, r.checkOut, lang)} · ${nights(lang, r.checkIn.daysUntil(r.checkOut))}",
                        style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Spacer(Modifier.height(10.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(r.ref, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.labelLarge, modifier = Modifier.weight(1f))
                        Text(money(r.totalEur), style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
                    }
                    if (active) {
                        Spacer(Modifier.height(16.dp))
                        if (Capabilities.digitalKey) {
                            LumbreButton(t(K.KEY_OPEN), { onKey(r.ref) }, Modifier.fillMaxWidth(), icon = Icons.Rounded.Key)
                        } else {
                            // En la web la llave no existe: lo indicamos en vez de esconderlo.
                            Row(
                                Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp))
                                    .padding(vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                Icon(Icons.Rounded.Smartphone, null, tint = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(8.dp))
                                Text(t(K.KEY_ONLY_APP), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                        if (r.status == ReservationStatus.CONFIRMED) {
                            TextButton(onClick = { cancelRef = r.ref }, modifier = Modifier.align(Alignment.End)) {
                                Text(t(K.CANCEL_BOOKING), color = MaterialTheme.colorScheme.error)
                            }
                        }
                    }
                }
            }
        }
    }

    cancelRef?.let { ref ->
        AlertDialog(
            onDismissRequest = { cancelRef = null },
            title = { Text(t(K.CANCEL_Q)) },
            text = { Text(t(K.CANCEL_Q_SUB)) },
            confirmButton = {
                TextButton(onClick = { repo.setStatus(ref, ReservationStatus.CANCELLED); cancelRef = null }) {
                    Text(t(K.CANCEL_BOOKING), color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = { TextButton(onClick = { cancelRef = null }) { Text(t(K.KEEP)) } },
        )
    }
}
