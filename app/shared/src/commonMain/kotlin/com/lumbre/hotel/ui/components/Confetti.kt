package com.lumbre.hotel.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.rotate
import kotlin.random.Random

private class Piece(val x: Float, val vx: Float, val vy: Float, val size: Float, val spin: Float, val color: Color, val round: Boolean)

private val confettiColors = listOf(Color(0xFF0F5F66), Color(0xFFE9B95C), Color(0xFFD9603B), Color(0xFF7FC8C4), Color(0xFFF3EBDD))

/** Explosión de confeti al confirmar la reserva. */
@Composable
fun ConfettiBurst(key: Any, modifier: Modifier = Modifier.fillMaxSize()) {
    val pieces = remember(key) {
        List(140) {
            Piece(
                x = 0.5f + (Random.nextFloat() - 0.5f) * 0.3f,
                vx = (Random.nextFloat() - 0.5f) * 1.6f,
                vy = -(Random.nextFloat() * 1.4f + 0.7f),
                size = Random.nextFloat() * 9f + 6f,
                spin = (Random.nextFloat() - 0.5f) * 720f,
                color = confettiColors[Random.nextInt(confettiColors.size)],
                round = Random.nextFloat() < 0.3f,
            )
        }
    }
    var time by remember(key) { mutableFloatStateOf(0f) }
    LaunchedEffect(key) {
        val start = withFrameNanos { it }
        while (time < 3.2f) {
            val now = withFrameNanos { it }
            time = (now - start) / 1_000_000_000f
        }
    }
    if (time >= 3.2f) return
    Canvas(modifier) {
        val g = 1.9f
        val alpha = (1f - ((time - 2.2f) / 1f)).coerceIn(0f, 1f)
        for (p in pieces) {
            val x = (p.x + p.vx * time * 0.5f) * size.width
            val y = size.height * 0.62f + (p.vy * time + 0.5f * g * time * time) * size.height * 0.5f
            rotate(p.spin * time, pivot = Offset(x, y)) {
                if (p.round) drawCircle(p.color.copy(alpha = alpha), p.size / 2.2f, Offset(x, y))
                else drawRect(p.color.copy(alpha = alpha), topLeft = Offset(x - p.size / 2, y - p.size / 3), size = Size(p.size, p.size * 0.6f))
            }
        }
    }
}
