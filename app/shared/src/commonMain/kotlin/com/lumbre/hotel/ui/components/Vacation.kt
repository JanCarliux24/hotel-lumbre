package com.lumbre.hotel.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.BeachAccess
import androidx.compose.material.icons.rounded.FamilyRestroom
import androidx.compose.material.icons.rounded.Pool
import androidx.compose.material.icons.rounded.Restaurant
import androidx.compose.material.icons.rounded.Sailing
import androidx.compose.material.icons.rounded.Spa
import androidx.compose.material.icons.rounded.WbSunny
import androidx.compose.material.icons.rounded.WbTwilight
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlin.math.PI
import kotlin.math.sin

/**
 * Olas animadas: tres capas que se desplazan a distinta velocidad.
 * Se coloca en el borde inferior de una foto para "fundirla" con el fondo.
 */
@Composable
fun WavesEdge(color: Color, modifier: Modifier = Modifier, height: Dp = 56.dp) {
    val inf = rememberInfiniteTransition(label = "waves")
    val phase by inf.animateFloat(0f, (2 * PI).toFloat(), infiniteRepeatable(tween(7000, easing = LinearEasing)), label = "phase")
    Canvas(modifier.fillMaxWidth().height(height)) {
        val layers = listOf(
            Triple(0.35f, 1.0f, 0.55f), // alfa, velocidad, altura relativa de la cresta
            Triple(0.6f, -1.4f, 0.4f),
            Triple(1f, 0.8f, 0.25f),
        )
        layers.forEachIndexed { i, (alpha, speed, crest) ->
            val path = Path()
            val base = size.height * (0.35f + i * 0.18f)
            val amp = size.height * crest * 0.45f
            path.moveTo(0f, size.height)
            var x = 0f
            while (x <= size.width + 8f) {
                val y = base + amp * sin((x / size.width) * 2 * PI.toFloat() * 1.6f + phase * speed + i)
                path.lineTo(x, y)
                x += 8f
            }
            path.lineTo(size.width, size.height); path.close()
            drawPath(path, color.copy(alpha = alpha))
        }
    }
}

/** Superficie translúcida tipo cristal (sobre fotos y degradados). */
fun Modifier.glass(shape: Shape, tint: Color, borderAlpha: Float = 0.7f): Modifier =
    this.background(tint, shape).border(1.dp, Color.White.copy(alpha = borderAlpha), shape)

/** Icono que flota y se balancea suavemente (sol, sombrilla, velero…). */
@Composable
fun FloatingIcon(icon: ImageVector, tint: Color, modifier: Modifier = Modifier, size: Dp = 22.dp, delayMs: Int = 0) {
    val inf = rememberInfiniteTransition(label = "float")
    val y by inf.animateFloat(-4f, 4f, infiniteRepeatable(tween(1800 + delayMs % 600), RepeatMode.Reverse), label = "y")
    val r by inf.animateFloat(-8f, 8f, infiniteRepeatable(tween(2400 + delayMs % 900), RepeatMode.Reverse), label = "r")
    Icon(icon, null, tint = tint, modifier = modifier.size(size).graphicsLayer { translationY = y; rotationZ = r })
}

private val vibes = listOf(
    Icons.Rounded.BeachAccess to K.VIBE_BEACH,
    Icons.Rounded.WbSunny to K.VIBE_SUN,
    Icons.Rounded.Spa to K.VIBE_SPA,
    Icons.Rounded.Restaurant to K.VIBE_FOOD,
    Icons.Rounded.Sailing to K.VIBE_SAIL,
    Icons.Rounded.WbTwilight to K.VIBE_SUNSET,
    Icons.Rounded.Pool to K.VIBE_POOL,
    Icons.Rounded.FamilyRestroom to K.VIBE_FAMILY,
)

/** Cinta continua con los "momentos" de las vacaciones. */
@Composable
fun VibesMarquee(modifier: Modifier = Modifier) {
    val inf = rememberInfiniteTransition(label = "marquee")
    val progress by inf.animateFloat(0f, 1f, infiniteRepeatable(tween(32000, easing = LinearEasing)), label = "p")
    var contentWidth by remember { mutableIntStateOf(0) }
    val ex = LocalExtras.current
    val colors = listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.secondary, MaterialTheme.colorScheme.tertiary)
    Box(modifier.fillMaxWidth().clipToBounds()) {
        Row(
            Modifier.wrapContentWidth(Alignment.Start, unbounded = true)
                .onSizeChanged { contentWidth = it.width }
                .graphicsLayer { translationX = -progress * contentWidth / 2f },
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            repeat(2) {
                vibes.forEachIndexed { i, (icon, label) ->
                    Row(
                        Modifier.background(if (i % 2 == 0) ex.sky else ex.sand, RoundedCornerShape(50))
                            .padding(horizontal = 16.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Icon(icon, null, tint = colors[i % colors.size], modifier = Modifier.size(20.dp))
                        Spacer(Modifier.width(8.dp))
                        Text(t(label), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurface)
                    }
                }
            }
        }
    }
}
