package com.lumbre.hotel.ui.screens

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.CalendarMonth
import androidx.compose.material.icons.rounded.Language
import androidx.compose.material.icons.rounded.People
import androidx.compose.material.icons.rounded.Star
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.RoomId
import com.lumbre.hotel.data.today
import com.lumbre.hotel.domain.Format
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.nights
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.resources.Res
import com.lumbre.hotel.resources.hero
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.LocalCurrency
import com.lumbre.hotel.ui.components.LocalWide
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.PhotoCard
import com.lumbre.hotel.ui.components.SectionHeader
import com.lumbre.hotel.ui.components.Stepper
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.bounceClick
import com.lumbre.hotel.ui.components.money
import com.lumbre.hotel.ui.components.sharedBounds
import com.lumbre.hotel.ui.navigation.BookingRoute
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlinx.coroutines.delay
import kotlinx.datetime.DateTimeUnit
import kotlinx.datetime.daysUntil
import kotlinx.datetime.plus
import org.jetbrains.compose.resources.painterResource

@Composable
fun HomeScreen(onRoom: (RoomId) -> Unit, onBook: (BookingRoute) -> Unit, onSeeRooms: () -> Unit, onOpenPrefs: () -> Unit) {
    val wide = LocalWide.current
    val list = rememberLazyListState()
    val heroHeight = if (wide) 620.dp else 560.dp

    LazyColumn(state = list, modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(bottom = 32.dp)) {
        item(key = "hero") {
            val scroll by remember { derivedStateOf { if (list.firstVisibleItemIndex == 0) list.firstVisibleItemScrollOffset else 2000 } }
            Box(Modifier.fillMaxWidth().height(heroHeight).clipToBounds()) {
                Image(
                    painterResource(Res.drawable.hero), null, contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize().graphicsLayer {
                        translationY = scroll * 0.45f
                        val s = 1.08f + scroll / 4000f
                        scaleX = s; scaleY = s
                    },
                )
                Box(
                    Modifier.fillMaxSize().background(
                        Brush.verticalGradient(0f to Color(0x99081E22), 0.4f to Color(0x33081E22), 1f to Color(0xCC081E22))
                    )
                )
                HeroHeader(onOpenPrefs)
                MaxWidth(Modifier.align(Alignment.BottomCenter)) {
                    Column(
                        Modifier.padding(horizontal = 24.dp).padding(bottom = 96.dp)
                            .graphicsLayer { alpha = 1f - (scroll / 600f).coerceIn(0f, 1f); translationY = -scroll * 0.15f },
                    ) {
                        Text(t(K.HERO_EYEBROW).uppercase(), color = Color.White.copy(alpha = 0.9f), style = MaterialTheme.typography.labelLarge, modifier = Modifier.appear(0))
                        Spacer(Modifier.height(12.dp))
                        Text(
                            t(K.HERO_TITLE), color = Color.White,
                            style = if (wide) MaterialTheme.typography.displayLarge else MaterialTheme.typography.displaySmall,
                            modifier = Modifier.appear(1, 80f),
                        )
                        Spacer(Modifier.height(12.dp))
                        Text(t(K.HERO_SUB), color = Color.White.copy(alpha = 0.92f), style = MaterialTheme.typography.bodyLarge, modifier = Modifier.appear(2))
                    }
                }
            }
        }
        item(key = "quick") {
            MaxWidth(Modifier.offset(y = (-64).dp).padding(horizontal = 16.dp)) { QuickSearch(onBook) }
        }
        item(key = "rooms-head") {
            MaxWidth(Modifier.padding(horizontal = 24.dp)) {
                SectionHeader(t(K.SEC_ROOMS_EYEBROW), t(K.SEC_ROOMS_TITLE), Modifier.appear()) {
                    TextButton(onClick = onSeeRooms) { Text(t(K.SEE_ALL)) }
                }
            }
            Spacer(Modifier.height(16.dp))
        }
        item(key = "rooms") { RoomCarousel(onRoom) }
        item(key = "exp") {
            Spacer(Modifier.height(48.dp))
            MaxWidth(Modifier.padding(horizontal = 24.dp)) {
                Column {
                    SectionHeader(t(K.SEC_EXP_EYEBROW), t(K.SEC_EXP_TITLE), Modifier.appear())
                    Spacer(Modifier.height(16.dp))
                    val columns = if (wide) 3 else 2
                    Catalog.experiences.chunked(columns).forEachIndexed { row, chunk ->
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.padding(bottom = 12.dp)) {
                            chunk.forEachIndexed { i, tile ->
                                PhotoCard(tile.image, Modifier.weight(1f).aspectRatio(if (wide) 1.25f else 0.85f).appear(row * columns + i)) {
                                    Column(Modifier.align(Alignment.BottomStart).padding(16.dp)) {
                                        Text(t(tile.title), color = Color.White, style = MaterialTheme.typography.titleMedium)
                                        Text(t(tile.sub), color = Color.White.copy(alpha = 0.85f), style = MaterialTheme.typography.bodySmall)
                                    }
                                }
                            }
                            repeat(columns - chunk.size) { Spacer(Modifier.weight(1f)) }
                        }
                    }
                }
            }
        }
        item(key = "dest") {
            Spacer(Modifier.height(36.dp))
            MaxWidth(Modifier.padding(horizontal = 24.dp)) { SectionHeader(t(K.SEC_DEST_EYEBROW), t(K.SEC_DEST_TITLE), Modifier.appear()) }
            Spacer(Modifier.height(16.dp))
            LazyRow(contentPadding = PaddingValues(horizontal = 24.dp), horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                itemsIndexed(Catalog.destinations) { i, d ->
                    PhotoCard(d.image, Modifier.width(220.dp).height(300.dp).appear(i)) {
                        Column(Modifier.align(Alignment.BottomStart).padding(16.dp)) {
                            Text(t(d.sub).uppercase(), color = LocalExtras.current.gold.copy(alpha = 1f), style = MaterialTheme.typography.labelSmall)
                            Text(t(d.title), color = Color.White, style = MaterialTheme.typography.titleLarge)
                        }
                    }
                }
            }
        }
        item(key = "reviews") {
            Spacer(Modifier.height(44.dp))
            MaxWidth(Modifier.padding(horizontal = 24.dp)) { SectionHeader(t(K.SEC_REV_EYEBROW), t(K.SEC_REV_TITLE), Modifier.appear()) }
            Spacer(Modifier.height(16.dp))
            LazyRow(contentPadding = PaddingValues(horizontal = 24.dp), horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                items(Catalog.reviews) { (text, author) ->
                    Card(
                        Modifier.width(300.dp).appear(),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
                        shape = RoundedCornerShape(24.dp),
                    ) {
                        Column(Modifier.padding(20.dp)) {
                            Row { repeat(5) { Icon(Icons.Rounded.Star, null, tint = LocalExtras.current.gold, modifier = Modifier.size(18.dp)) } }
                            Spacer(Modifier.height(10.dp))
                            Text(t(text), style = MaterialTheme.typography.bodyLarge, minLines = 3)
                            Spacer(Modifier.height(12.dp))
                            Text(author, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
        item(key = "footer") {
            Spacer(Modifier.height(40.dp))
            HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
            MaxWidth(Modifier.padding(24.dp)) {
                Text(t(K.FOOTER), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun HeroHeader(onOpenPrefs: () -> Unit) {
    val currency = LocalCurrency.current
    val lang = LocalLang.current
    MaxWidth(Modifier.statusBarsPadding().padding(horizontal = 20.dp, vertical = 12.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Lumbre", color = Color.White, style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
            Surface(
                shape = RoundedCornerShape(50), color = Color.White.copy(alpha = 0.18f), contentColor = Color.White,
                modifier = Modifier.border(1.dp, Color.White.copy(alpha = 0.5f), RoundedCornerShape(50)).bounceClick(onClick = onOpenPrefs),
            ) {
                Row(Modifier.padding(horizontal = 14.dp, vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Rounded.Language, null, modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(6.dp))
                    Text("${lang.code.uppercase()} · ${currency.code}", style = MaterialTheme.typography.labelLarge)
                }
            }
        }
    }
}

@Composable
private fun QuickSearch(onBook: (BookingRoute) -> Unit) {
    val lang = LocalLang.current
    var start by remember { mutableStateOf(today().plus(14, DateTimeUnit.DAY)) }
    var end by remember { mutableStateOf(today().plus(17, DateTimeUnit.DAY)) }
    var guests by remember { mutableIntStateOf(2) }
    var picking by remember { mutableStateOf(false) }

    Card(
        shape = RoundedCornerShape(28.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
        elevation = CardDefaults.cardElevation(defaultElevation = 10.dp),
        modifier = Modifier.fillMaxWidth().appear(3, 90f),
    ) {
        Column(Modifier.padding(20.dp)) {
            Row(
                Modifier.fillMaxWidth().clip(RoundedCornerShape(18.dp)).background(MaterialTheme.colorScheme.surfaceContainerLow)
                    .bounceClick(scaleDown = 0.98f) { picking = true }.padding(16.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Icon(Icons.Rounded.CalendarMonth, null, tint = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(t(K.QS_DATES), style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(Format.range(start, end, lang), style = MaterialTheme.typography.titleMedium)
                }
                Text(nights(lang, start.daysUntil(end)), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
            }
            Spacer(Modifier.height(12.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(start = 16.dp)) {
                Icon(Icons.Rounded.People, null, tint = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.width(12.dp))
                Stepper(t(K.QS_GUESTS), null, guests, 1..6, { guests = it }, Modifier.weight(1f))
            }
            Spacer(Modifier.height(16.dp))
            LumbreButton(
                t(K.QS_CTA),
                onClick = { onBook(BookingRoute(checkIn = start.toString(), checkOut = end.toString(), guests = guests)) },
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
    if (picking) {
        DateRangeDialog(start, end, onDismiss = { picking = false }) { s, e -> start = s; end = e; picking = false }
    }
}

@Composable
private fun RoomCarousel(onRoom: (RoomId) -> Unit) {
    val rooms by AppGraph.repo.rooms.collectAsState()
    LazyRow(contentPadding = PaddingValues(horizontal = 24.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
        itemsIndexed(Catalog.rooms, key = { _, r -> r.id.name }) { i, info ->
            val cfg = rooms.first { it.id == info.id }
            Column(Modifier.width(290.dp).appear(i).bounceClick(scaleDown = 0.97f) { onRoom(info.id) }) {
                Box {
                    Image(
                        painterResource(info.image), null, contentScale = ContentScale.Crop,
                        modifier = Modifier.sharedBounds("room-${info.id}").fillMaxWidth().height(210.dp).clip(RoundedCornerShape(24.dp)),
                    )
                    if (info.popular) Badge(t(K.POPULAR), Modifier.padding(12.dp))
                    if (!cfg.available) Badge(t(K.UNAVAILABLE), Modifier.padding(12.dp).align(Alignment.TopEnd), danger = true)
                }
                Spacer(Modifier.height(12.dp))
                Text(t(info.name), style = MaterialTheme.typography.titleLarge)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("${t(K.FROM)} ", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(money(cfg.nightlyEur.toDouble()), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                    Text(" ${t(K.PER_NIGHT)}", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

@Composable
fun Badge(text: String, modifier: Modifier = Modifier, danger: Boolean = false) {
    val bounce = remember { Animatable(0.6f) }
    LaunchedEffect(Unit) { delay(300); bounce.animateTo(1f, spring(dampingRatio = 0.4f, stiffness = 300f)) }
    Text(
        text,
        style = MaterialTheme.typography.labelMedium,
        color = if (danger) MaterialTheme.colorScheme.onError else MaterialTheme.colorScheme.primary,
        modifier = modifier
            .graphicsLayer { scaleX = bounce.value; scaleY = bounce.value }
            .clip(RoundedCornerShape(50))
            .background(if (danger) MaterialTheme.colorScheme.error else Color.White)
            .padding(horizontal = 12.dp, vertical = 6.dp),
    )
}
