package com.lumbre.hotel.ui.components

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.keyframes
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.scaleIn
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.ui.theme.Palette

enum class Mood { Happy, Sad, Party, Think }

/** Lumi, la mascota del hotel (una campana de recepción). Reacciona a lo que pasa en el formulario. */
@Composable
fun Lumi(mood: Mood, trigger: Any, modifier: Modifier = Modifier.size(76.dp)) {
    val inf = rememberInfiniteTransition(label = "lumi")
    val breathe by inf.animateFloat(1f, 1.035f, infiniteRepeatable(tween(1600, easing = FastOutSlowInEasing), RepeatMode.Reverse), label = "breathe")
    val blink by inf.animateFloat(
        1f, 1f,
        infiniteRepeatable(keyframes { durationMillis = 4200; 1f at 3800; 0.1f at 3920; 1f at 4060 }),
        label = "blink",
    )
    val jump = remember { Animatable(0f) }
    val tilt = remember { Animatable(0f) }
    LaunchedEffect(trigger) {
        when (mood) {
            Mood.Party -> repeat(2) {
                jump.animateTo(-26f, tween(160)); jump.animateTo(0f, spring(dampingRatio = 0.35f, stiffness = 500f))
            }
            Mood.Sad -> {
                tilt.animateTo(-9f, tween(80)); tilt.animateTo(8f, tween(110)); tilt.animateTo(-4f, tween(90)); tilt.animateTo(0f, spring())
            }
            else -> {
                jump.animateTo(-12f, tween(140)); jump.animateTo(0f, spring(dampingRatio = 0.4f, stiffness = 420f))
            }
        }
    }
    val ink = Palette.Ink
    Canvas(modifier) {
        val k = size.width / 120f
        scale(k, k, pivot = Offset.Zero) {
            drawOval(Color(0x24000000), topLeft = Offset(22f, 98f), size = Size(76f, 10f))
            translate(top = jump.value) {
                rotate(tilt.value, pivot = Offset(60f, 94f)) {
                    scale(scaleX = 2f - breathe, scaleY = breathe, pivot = Offset(60f, 94f)) {
                        drawRoundRect(Palette.Gold, topLeft = Offset(54f, 8f), size = Size(12f, 14f), cornerRadius = androidx.compose.ui.geometry.CornerRadius(6f))
                        val dome = Path().apply {
                            moveTo(16f, 82f); cubicTo(16f, 54f, 35f, 32f, 60f, 32f); cubicTo(85f, 32f, 104f, 54f, 104f, 82f); close()
                        }
                        drawPath(dome, Palette.GoldLight)
                        drawPath(
                            Path().apply { moveTo(28f, 70f); cubicTo(30f, 54f, 39f, 43f, 51f, 39f) },
                            Color.White.copy(alpha = 0.6f), style = Stroke(5f, cap = StrokeCap.Round),
                        )
                        drawRoundRect(Palette.Sea, topLeft = Offset(8f, 80f), size = Size(104f, 14f), cornerRadius = androidx.compose.ui.geometry.CornerRadius(7f))
                        // ojos
                        val eyeH = 13f * blink
                        drawOval(ink, topLeft = Offset(41f, 60f - eyeH / 2), size = Size(10f, eyeH))
                        drawOval(ink, topLeft = Offset(69f, 60f - eyeH / 2), size = Size(10f, eyeH))
                        // mejillas
                        drawCircle(Color(0x55D9603B), 5f, Offset(34f, 70f))
                        drawCircle(Color(0x55D9603B), 5f, Offset(86f, 70f))
                        val mouth = Path().apply {
                            when (mood) {
                                Mood.Sad -> { moveTo(50f, 76f); quadraticTo(60f, 68f, 70f, 76f) }
                                Mood.Party -> { moveTo(52f, 69f); quadraticTo(60f, 80f, 68f, 69f); close() }
                                Mood.Think -> { moveTo(53f, 72f); lineTo(67f, 72f) }
                                Mood.Happy -> { moveTo(50f, 70f); quadraticTo(60f, 78f, 70f, 70f) }
                            }
                        }
                        if (mood == Mood.Party) drawPath(mouth, ink) else drawPath(mouth, ink, style = Stroke(3.5f, cap = StrokeCap.Round))
                    }
                }
            }
        }
    }
}

/** Lumi con bocadillo de texto que cambia con animación. */
@Composable
fun LumiSays(text: String, mood: Mood, modifier: Modifier = Modifier, trigger: Any = text) {
    Row(modifier, verticalAlignment = Alignment.Bottom) {
        Lumi(mood, trigger = trigger)
        Spacer(Modifier.width(10.dp))
        AnimatedContent(
            targetState = text,
            transitionSpec = { (scaleIn(initialScale = 0.85f, animationSpec = spring(dampingRatio = 0.5f)) + fadeIn()) togetherWith fadeOut(tween(90)) },
            label = "bubble",
        ) { msg ->
            Text(
                msg, style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier
                    .clip(RoundedCornerShape(20.dp, 20.dp, 20.dp, 4.dp))
                    .background(MaterialTheme.colorScheme.surfaceContainer)
                    .padding(horizontal = 16.dp, vertical = 12.dp),
            )
        }
    }
}
