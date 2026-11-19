package com.lumbre.hotel.ui.screens

import androidx.compose.foundation.background
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
import androidx.compose.material.icons.rounded.CalendarMonth
import androidx.compose.material.icons.rounded.LocalOffer
import androidx.compose.material.icons.rounded.NightsStay
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.FloatingIcon
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.WavesEdge
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.navigation.BookingRoute
import com.lumbre.hotel.ui.theme.Palette

@Composable
fun OffersScreen(onBook: (BookingRoute) -> Unit) {
    val repo = AppGraph.repo
    val promos by repo.promos.collectAsState()
    val params by repo.params.collectAsState()
    val active = promos.filter { it.active }.sortedByDescending { it.percent }

    LazyVerticalGrid(
        columns = GridCells.Adaptive(320.dp), modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item(span = { GridItemSpan(maxLineSpan) }) {
            Row(Modifier.statusBarsPadding().padding(top = 12.dp).appear(), verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text(t(K.OFF_TITLE), style = MaterialTheme.typography.displaySmall)
                    Text(t(K.OFF_SUB), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                FloatingIcon(Icons.Rounded.LocalOffer, MaterialTheme.colorScheme.tertiary, size = 40.dp)
            }
        }
        if (active.isEmpty()) item(span = { GridItemSpan(maxLineSpan) }) {
            Text(t(K.OFF_EMPTY), color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        itemsIndexed(active, key = { _, p -> p.code }) { i, promo ->
            Card(Modifier.appear(i), shape = RoundedCornerShape(28.dp), colors = CardDefaults.cardColors(containerColor = Color.Transparent)) {
                Box(
                    Modifier.fillMaxWidth().clip(RoundedCornerShape(28.dp))
                        .background(Brush.linearGradient(listOf(Palette.Turquoise, Color(0xFF13A3A8), Palette.Sun))),
                ) {
                    WavesEdge(Color.White.copy(alpha = 0.35f), Modifier.align(Alignment.BottomCenter), height = 46.dp)
                    Column(Modifier.padding(22.dp)) {
                        Text("−${promo.percent}%", style = MaterialTheme.typography.displayMedium, color = Color.White)
                        Text(t(K.OFF_PERCENT, promo.percent), color = Color.White.copy(alpha = 0.92f), style = MaterialTheme.typography.bodyLarge)
                        Spacer(Modifier.height(14.dp))
                        Text(
                            promo.code, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.titleLarge, color = Palette.Navy,
                            modifier = Modifier.clip(RoundedCornerShape(12.dp)).background(Color.White).padding(horizontal = 14.dp, vertical = 8.dp),
                        )
                        Spacer(Modifier.height(16.dp))
                        LumbreButton(t(K.OFF_USE), { onBook(BookingRoute(promo = promo.code)) }, kind = BtnKind.Secondary)
                        Spacer(Modifier.height(18.dp))
                    }
                }
            }
        }
        item(span = { GridItemSpan(maxLineSpan) }) {
            Card(Modifier.appear(active.size + 1), shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest)) {
                Column(Modifier.padding(20.dp)) {
                    Text(t(K.OFF_AUTO_TITLE), style = MaterialTheme.typography.titleLarge)
                    Spacer(Modifier.height(10.dp))
                    AutoRow(Icons.Rounded.NightsStay, t(K.OFF_LONGSTAY, params.longStayNights, params.longStayDiscountPercent))
                    AutoRow(Icons.Rounded.CalendarMonth, t(K.OFF_WEEKEND, params.weekendSurchargePercent))
                }
            }
        }
    }
}

@Composable
private fun AutoRow(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(Modifier.padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(22.dp))
        Spacer(Modifier.width(12.dp))
        Text(text, style = MaterialTheme.typography.bodyLarge)
    }
}
