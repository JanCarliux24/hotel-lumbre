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
import androidx.compose.material.icons.rounded.People
import androidx.compose.material.icons.rounded.SquareFoot
import androidx.compose.material.icons.rounded.Star
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
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.bounceClick
import com.lumbre.hotel.ui.components.money
import com.lumbre.hotel.ui.components.sharedBounds
import com.lumbre.hotel.ui.theme.LocalExtras
import org.jetbrains.compose.resources.painterResource

@Composable
fun RoomsScreen(onRoom: (RoomId) -> Unit) {
    val rooms by AppGraph.repo.rooms.collectAsState()
    LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = 340.dp),
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item(span = { GridItemSpan(maxLineSpan) }) {
            Column(Modifier.statusBarsPadding().padding(top = 12.dp, bottom = 8.dp).appear()) {
                Text(t(K.ROOMS_TITLE), style = MaterialTheme.typography.displaySmall)
                Spacer(Modifier.height(6.dp))
                Text(t(K.ROOMS_SUB), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        itemsIndexed(Catalog.rooms, key = { _, r -> r.id.name }) { i, info ->
            val cfg = rooms.first { it.id == info.id }
            Card(
                shape = RoundedCornerShape(28.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
                elevation = CardDefaults.cardElevation(2.dp),
                modifier = Modifier.appear(i).bounceClick(scaleDown = 0.98f) { onRoom(info.id) },
            ) {
                Box {
                    Image(
                        painterResource(info.image), null, contentScale = ContentScale.Crop,
                        modifier = Modifier.sharedBounds("room-${info.id}").fillMaxWidth().height(230.dp)
                            .clip(RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp))
                            .graphicsLayer { alpha = if (cfg.available) 1f else 0.55f },
                    )
                    if (info.popular) Badge(t(K.POPULAR), Modifier.padding(14.dp))
                    if (!cfg.available) Badge(t(K.UNAVAILABLE), Modifier.padding(14.dp).align(Alignment.TopEnd), danger = true)
                }
                Column(Modifier.padding(20.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(t(info.name), style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
                        Icon(Icons.Rounded.Star, null, tint = LocalExtras.current.gold, modifier = Modifier.size(18.dp))
                        Text(" ${info.rating}", style = MaterialTheme.typography.labelLarge)
                    }
                    Spacer(Modifier.height(6.dp))
                    Text(t(info.description), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(14.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        MetaChip(Icons.Rounded.People, t(K.CAPACITY, cfg.capacity))
                        Spacer(Modifier.width(16.dp))
                        MetaChip(Icons.Rounded.SquareFoot, "${info.sizeM2} m²")
                        Spacer(Modifier.weight(1f))
                        Text(money(cfg.nightlyEur.toDouble()), style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
                        Text(" ${t(K.PER_NIGHT)}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
fun MetaChip(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
        Spacer(Modifier.width(6.dp))
        Text(text, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
    }
}
