package com.lumbre.hotel.ui.components

import androidx.compose.animation.AnimatedVisibilityScope
import androidx.compose.animation.SharedTransitionScope
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.Remove
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.ripple
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.Currency
import com.lumbre.hotel.data.ReservationStatus
import com.lumbre.hotel.domain.Format
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlinx.coroutines.delay
import org.jetbrains.compose.resources.DrawableResource
import org.jetbrains.compose.resources.painterResource

// ---------- Contexto compartido entre pantallas ----------
val LocalCurrency = staticCompositionLocalOf { Currency.EUR }
val LocalSnackbar = staticCompositionLocalOf { SnackbarHostState() }
val LocalSharedScope = compositionLocalOf<SharedTransitionScope?> { null }
val LocalNavScope = compositionLocalOf<AnimatedVisibilityScope?> { null }
val LocalWide = compositionLocalOf { false }

@Composable
fun money(eur: Double): String = Format.money(eur, LocalCurrency.current, LocalLang.current)

/** Imagen que "vuela" entre pantallas (transición de elemento compartido). */
@Composable
fun Modifier.sharedBounds(key: String): Modifier {
    val shared = LocalSharedScope.current ?: return this
    val nav = LocalNavScope.current ?: return this
    return with(shared) {
        this@sharedBounds.sharedElement(rememberSharedContentState(key), nav)
    }
}

// ---------- Microinteracciones ----------

/** Pulsación con rebote elástico y vibración ligera (estilo Duolingo). */
fun Modifier.bounceClick(enabled: Boolean = true, scaleDown: Float = 0.95f, onClick: () -> Unit): Modifier = composed {
    val interaction = remember { MutableInteractionSource() }
    val pressed by interaction.collectIsPressedAsState()
    val scale by animateFloatAsState(
        if (pressed && enabled) scaleDown else 1f,
        spring(dampingRatio = 0.42f, stiffness = Spring.StiffnessMediumLow), label = "bounce",
    )
    val haptic = LocalHapticFeedback.current
    graphicsLayer { scaleX = scale; scaleY = scale }
        .clickable(interactionSource = interaction, indication = ripple(), enabled = enabled, role = Role.Button) {
            haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
            onClick()
        }
}

/** Aparición escalonada al entrar en pantalla (estilo Apple). */
fun Modifier.appear(index: Int = 0, offsetY: Float = 56f): Modifier = composed {
    val progress = remember { Animatable(0f) }
    LaunchedEffect(Unit) {
        delay(index.coerceAtMost(8) * 70L)
        progress.animateTo(1f, spring(dampingRatio = 0.82f, stiffness = 180f))
    }
    graphicsLayer {
        alpha = progress.value.coerceIn(0f, 1f)
        translationY = (1f - progress.value) * offsetY
        val s = 0.97f + 0.03f * progress.value
        scaleX = s; scaleY = s
    }
}

enum class BtnKind { Primary, Secondary, Gold, Danger }

/** Botón "táctil" con canto inferior que se hunde al pulsar. */
@Composable
fun LumbreButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    kind: BtnKind = BtnKind.Primary,
    enabled: Boolean = true,
    icon: ImageVector? = null,
    height: Dp = 52.dp,
) {
    val cs = MaterialTheme.colorScheme
    val face: Color; val edge: Color; val content: Color; val stroke: Color?
    when (kind) {
        BtnKind.Primary -> { face = cs.primary; edge = lerp(cs.primary, Color.Black, 0.32f); content = cs.onPrimary; stroke = null }
        BtnKind.Gold -> { face = cs.secondary; edge = lerp(cs.secondary, Color.Black, 0.3f); content = cs.onSecondary; stroke = null }
        BtnKind.Danger -> { face = cs.error; edge = lerp(cs.error, Color.Black, 0.3f); content = cs.onError; stroke = null }
        BtnKind.Secondary -> { face = cs.surfaceContainerLowest; edge = cs.outlineVariant; content = cs.onSurface; stroke = cs.outlineVariant }
    }
    val depth = 4.dp
    val interaction = remember { MutableInteractionSource() }
    val pressed by interaction.collectIsPressedAsState()
    val press by animateDpAsState(if (pressed && enabled) depth else 0.dp, spring(stiffness = Spring.StiffnessHigh), label = "press")
    val haptic = LocalHapticFeedback.current
    val radius = height / 2

    Row(
        modifier
            .graphicsLayer { alpha = if (enabled) 1f else 0.45f }
            .height(height + depth)
            .widthIn(min = 64.dp)
            .clickable(interactionSource = interaction, indication = null, enabled = enabled, role = Role.Button) {
                haptic.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                onClick()
            }
            .drawBehind {
                val d = depth.toPx(); val p = press.toPx(); val r = CornerRadius(radius.toPx())
                val h = size.height - d
                drawRoundRect(edge, topLeft = Offset(0f, d), size = Size(size.width, h), cornerRadius = r)
                drawRoundRect(face, topLeft = Offset(0f, p), size = Size(size.width, h), cornerRadius = r)
                if (stroke != null) drawRoundRect(stroke, topLeft = Offset(0f, p), size = Size(size.width, h), cornerRadius = r, style = Stroke(1.5.dp.toPx()))
            }
            .padding(top = press, bottom = depth - press)
            .padding(horizontal = 24.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center,
    ) {
        if (icon != null) {
            Icon(icon, null, tint = content, modifier = Modifier.size(20.dp))
            Spacer(Modifier.width(10.dp))
        }
        Text(text, color = content, style = MaterialTheme.typography.labelLarge, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@Composable
fun SectionHeader(eyebrow: String, title: String, modifier: Modifier = Modifier, action: (@Composable () -> Unit)? = null) {
    Row(modifier.fillMaxWidth(), verticalAlignment = Alignment.Bottom) {
        Column(Modifier.weight(1f)) {
            Text(eyebrow.uppercase(), style = MaterialTheme.typography.labelMedium, color = LocalExtras.current.gold)
            Spacer(Modifier.height(6.dp))
            Text(title, style = MaterialTheme.typography.headlineMedium)
        }
        action?.invoke()
    }
}

@Composable
fun Stepper(label: String, hint: String?, value: Int, range: IntRange, onChange: (Int) -> Unit, modifier: Modifier = Modifier) {
    Row(modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Column(Modifier.weight(1f)) {
            Text(label, style = MaterialTheme.typography.titleMedium)
            if (hint != null) Text(hint, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        RoundIconButton(Icons.Rounded.Remove, "−", enabled = value > range.first) { onChange(value - 1) }
        val scale = remember { Animatable(1f) }
        LaunchedEffect(value) { scale.snapTo(1.25f); scale.animateTo(1f, spring(dampingRatio = 0.4f, stiffness = 500f)) }
        Text(
            value.toString(), style = MaterialTheme.typography.titleLarge,
            modifier = Modifier.width(48.dp).graphicsLayer { scaleX = scale.value; scaleY = scale.value },
            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
        )
        RoundIconButton(Icons.Rounded.Add, "+", enabled = value < range.last) { onChange(value + 1) }
    }
}

@Composable
fun RoundIconButton(icon: ImageVector, description: String, enabled: Boolean = true, onClick: () -> Unit) {
    Surface(
        shape = CircleShape,
        color = if (enabled) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceContainerHigh,
        contentColor = if (enabled) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.outline,
        modifier = Modifier.size(44.dp).semantics { contentDescription = description }.bounceClick(enabled, 0.85f, onClick),
    ) { Box(contentAlignment = Alignment.Center) { Icon(icon, null) } }
}

/** Foto a sangre con degradado y contenido encima. */
@Composable
fun PhotoCard(
    image: DrawableResource,
    modifier: Modifier = Modifier,
    imageModifier: Modifier = Modifier,
    shape: RoundedCornerShape = RoundedCornerShape(24.dp),
    onClick: (() -> Unit)? = null,
    content: @Composable BoxScope.() -> Unit,
) {
    Box(
        modifier
            .clip(shape)
            .then(if (onClick != null) Modifier.bounceClick(scaleDown = 0.97f, onClick = onClick) else Modifier),
    ) {
        Image(painterResource(image), null, contentScale = ContentScale.Crop, modifier = Modifier.fillMaxSize().then(imageModifier))
        Box(
            Modifier.fillMaxSize().background(
                Brush.verticalGradient(0.35f to Color.Transparent, 1f to Color(0xD9061416))
            )
        )
        content()
    }
}

/** Limita el ancho del contenido en pantallas grandes (web y tablets). */
@Composable
fun MaxWidth(modifier: Modifier = Modifier, max: Dp = 1120.dp, content: @Composable () -> Unit) {
    Box(modifier.fillMaxWidth(), contentAlignment = Alignment.TopCenter) {
        Box(Modifier.widthIn(max = max).fillMaxWidth()) { content() }
    }
}

@Composable
fun StatusChip(status: ReservationStatus) {
    val ex = LocalExtras.current
    val cs = MaterialTheme.colorScheme
    val (bg, fg) = when (status) {
        ReservationStatus.CONFIRMED -> ex.okContainer to ex.ok
        ReservationStatus.CHECKED_IN -> cs.primaryContainer to cs.onPrimaryContainer
        ReservationStatus.CANCELLED -> cs.errorContainer to cs.error
    }
    Text(
        t(Catalog.status(status)),
        style = MaterialTheme.typography.labelMedium, color = fg,
        modifier = Modifier.clip(RoundedCornerShape(50)).background(bg).padding(horizontal = 12.dp, vertical = 6.dp),
    )
}

/** Precio que cuenta hacia el nuevo valor cuando cambia. */
@Composable
fun AnimatedMoney(eur: Double, style: androidx.compose.ui.text.TextStyle, color: Color = Color.Unspecified, modifier: Modifier = Modifier) {
    val animated by animateFloatAsState(eur.toFloat(), tween(650), label = "money")
    val bump = remember { Animatable(1f) }
    LaunchedEffect(eur) { bump.snapTo(1.08f); bump.animateTo(1f, spring(dampingRatio = 0.45f, stiffness = 380f)) }
    Text(
        money(animated.toDouble()), style = style, color = color, fontWeight = FontWeight.Bold,
        modifier = modifier.graphicsLayer { scaleX = bump.value; scaleY = bump.value },
    )
}
