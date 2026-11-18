package com.lumbre.hotel.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.EventAvailable
import androidx.compose.material.icons.rounded.People
import androidx.compose.material.icons.rounded.SquareFoot
import androidx.compose.material.icons.rounded.Star
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.LocalWide
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.bounceClick
import com.lumbre.hotel.ui.components.money
import com.lumbre.hotel.ui.components.sharedBounds
import com.lumbre.hotel.ui.theme.LocalExtras
import org.jetbrains.compose.resources.painterResource

@Composable
fun RoomDetailScreen(roomName: String, onBack: () -> Unit, onBook: () -> Unit) {
    val id = RoomId.entries.firstOrNull { it.name == roomName } ?: RoomId.DELUXE
    val info = Catalog.room(id)
    val rooms by AppGraph.repo.rooms.collectAsState()
    val cfg = rooms.first { it.id == id }
    val scroll = rememberScrollState()
    val wide = LocalWide.current

    Box(Modifier.fillMaxSize()) {
        Column(Modifier.fillMaxSize().verticalScroll(scroll).padding(bottom = 120.dp)) {
            Box(Modifier.fillMaxWidth().height(if (wide) 460.dp else 380.dp).clipToBounds()) {
                Image(
                    painterResource(info.image), t(info.name), contentScale = ContentScale.Crop,
                    modifier = Modifier.sharedBounds("room-${info.id}").fillMaxSize()
                        .graphicsLayer { translationY = scroll.value * 0.4f },
                )
                Box(Modifier.fillMaxWidth().height(120.dp).background(Brush.verticalGradient(listOf(Color(0x88000000), Color.Transparent))))
            }
            MaxWidth(Modifier.padding(horizontal = 24.dp), max = 900.dp) {
                Column {
                    Spacer(Modifier.height(24.dp))
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.appear(0)) {
                        Icon(Icons.Rounded.Star, null, tint = LocalExtras.current.gold, modifier = Modifier.size(18.dp))
                        Text(" " + t(K.RATING, info.rating, info.reviews), style = MaterialTheme.typography.labelLarge)
                        if (info.popular) { Spacer(Modifier.width(10.dp)); Badge(t(K.POPULAR)) }
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(t(info.name), style = MaterialTheme.typography.displaySmall, modifier = Modifier.appear(1))
                    Spacer(Modifier.height(10.dp))
                    Text(t(info.description), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.appear(2))
                    Spacer(Modifier.height(18.dp))
                    Row(Modifier.appear(3)) {
                        MetaChip(Icons.Rounded.People, t(K.CAPACITY, cfg.capacity))
                        Spacer(Modifier.width(20.dp))
                        MetaChip(Icons.Rounded.SquareFoot, "${info.sizeM2} m²")
                    }
                    Spacer(Modifier.height(28.dp))
                    Text(t(K.AMENITIES), style = MaterialTheme.typography.titleLarge, modifier = Modifier.appear(4))
                    Spacer(Modifier.height(12.dp))
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        info.amenities.forEachIndexed { i, (icon, label) ->
                            Row(
                                Modifier.appear(5 + i).clip(RoundedCornerShape(16.dp)).background(MaterialTheme.colorScheme.surfaceContainer)
                                    .padding(horizontal = 14.dp, vertical = 12.dp),
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                Icon(icon, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(20.dp))
                                Spacer(Modifier.width(8.dp))
                                Text(t(label), style = MaterialTheme.typography.labelLarge)
                            }
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Rounded.EventAvailable, null, tint = LocalExtras.current.ok)
                        Spacer(Modifier.width(8.dp))
                        Text(t(K.FREE_CANCEL), style = MaterialTheme.typography.bodyMedium, color = LocalExtras.current.ok)
                    }
                }
            }
        }

        Surface(
            shape = CircleShape, color = Color.Black.copy(alpha = 0.35f), contentColor = Color.White,
            modifier = Modifier.statusBarsPadding().padding(12.dp).size(44.dp).bounceClick(scaleDown = 0.85f, onClick = onBack),
        ) { Box(contentAlignment = Alignment.Center) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, t(K.BACK)) } }

        Surface(
            color = MaterialTheme.colorScheme.surfaceContainerLowest, shadowElevation = 16.dp,
            shape = RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp),
            modifier = Modifier.align(Alignment.BottomCenter).fillMaxWidth(),
        ) {
            MaxWidth(Modifier.navigationBarsPadding().padding(horizontal = 24.dp, vertical = 16.dp), max = 900.dp) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text(t(K.FROM), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Row(verticalAlignment = Alignment.Bottom) {
                            Text(money(cfg.nightlyEur.toDouble()), style = MaterialTheme.typography.headlineSmall, color = MaterialTheme.colorScheme.primary)
                            Text(" ${t(K.PER_NIGHT)}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    LumbreButton(
                        if (cfg.available) t(K.BOOK_NOW) else t(K.UNAVAILABLE),
                        onClick = onBook, enabled = cfg.available,
                    )
                }
            }
        }
    }
}
