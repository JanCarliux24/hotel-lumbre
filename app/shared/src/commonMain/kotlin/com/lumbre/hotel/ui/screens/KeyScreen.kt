package com.lumbre.hotel.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.Key
import androidx.compose.material.icons.rounded.LockOpen
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.Catalog
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.theme.Palette
import kotlinx.coroutines.delay

/** Llave digital: solo en Android e iOS (en la web se muestra el motivo). */
@Composable
fun KeyScreen(ref: String, onClose: () -> Unit) {
    val res = AppGraph.repo.reservations.value.firstOrNull { it.ref == ref }
    val roomNumber = remember(ref) { 100 * (2 + (ref.hashCode() and 0x7fffffff) % 4) + (ref.hashCode() and 0x7fffffff) % 18 + 1 }
    val haptic = LocalHapticFeedback.current
    var opened by remember { mutableStateOf(false) }
    val inf = rememberInfiniteTransition(label = "nfc")
    val wave by inf.animateFloat(0f, 1f, infiniteRepeatable(tween(2200, easing = LinearEasing), RepeatMode.Restart), label = "wave")
    val pop = remember { Animatable(1f) }

    LaunchedEffect(opened) {
        if (opened) {
            pop.snapTo(0.8f); pop.animateTo(1f, spring(dampingRatio = 0.35f, stiffness = 300f))
            delay(3000); opened = false
        }
    }

    Box(
        Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Palette.SeaNight, Color(0xFF061416)))),
        contentAlignment = Alignment.Center,
    ) {
        IconButton(onClick = onClose, modifier = Modifier.align(Alignment.TopEnd).statusBarsPadding().padding(8.dp)) {
            Icon(Icons.Rounded.Close, t(K.CLOSE), tint = Color.White)
        }
        Column(
            Modifier.widthIn(max = 420.dp).fillMaxWidth().padding(28.dp).navigationBarsPadding(),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(t(K.KEY_TITLE).uppercase(), color = Palette.GoldLight, style = MaterialTheme.typography.labelLarge)
            Spacer(Modifier.height(6.dp))
            Text(t(K.KEY_ROOM, roomNumber), color = Color.White, style = MaterialTheme.typography.displaySmall)
            res?.let { Text(t(Catalog.room(it.room).name), color = Color.White.copy(alpha = 0.7f), style = MaterialTheme.typography.bodyLarge) }
            Spacer(Modifier.height(40.dp))
            Box(Modifier.size(260.dp), contentAlignment = Alignment.Center) {
                Canvas(Modifier.fillMaxSize()) {
                    for (i in 0 until 3) {
                        val p = (wave + i / 3f) % 1f
                        drawCircle(
                            color = (if (opened) Color(0xFF8FD6AE) else Palette.GoldLight).copy(alpha = (1f - p) * 0.55f),
                            radius = size.minDimension / 2f * (0.35f + 0.65f * p),
                            style = Stroke(width = 3.dp.toPx()),
                        )
                    }
                }
                Box(
                    Modifier.size(120.dp).graphicsLayer { scaleX = pop.value; scaleY = pop.value }.clip(CircleShape)
                        .background(if (opened) Color(0xFF1F7A4D) else Palette.Gold),
                    contentAlignment = Alignment.Center,
                ) {
                    AnimatedContent(opened, transitionSpec = { scaleIn(spring(dampingRatio = 0.5f)) + fadeIn() togetherWith fadeOut() }, label = "lock") { o ->
                        Icon(if (o) Icons.Rounded.LockOpen else Icons.Rounded.Key, null, tint = Color.White, modifier = Modifier.size(52.dp))
                    }
                }
            }
            Spacer(Modifier.height(36.dp))
            Text(
                when {
                    !Capabilities.digitalKey -> t(K.KEY_MOBILE_ONLY)
                    opened -> t(K.KEY_OPENED)
                    else -> t(K.KEY_HINT)
                },
                color = Color.White.copy(alpha = 0.85f), style = MaterialTheme.typography.bodyLarge, textAlign = TextAlign.Center,
            )
            Spacer(Modifier.height(24.dp))
            if (Capabilities.digitalKey) {
                LumbreButton(
                    t(K.KEY_UNLOCK),
                    onClick = { haptic.performHapticFeedback(HapticFeedbackType.LongPress); opened = true },
                    modifier = Modifier.fillMaxWidth(), kind = BtnKind.Gold, icon = Icons.Rounded.LockOpen, enabled = !opened,
                )
            }
        }
    }
}
