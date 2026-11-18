package com.lumbre.hotel.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.lumbre.hotel.resources.Res
import com.lumbre.hotel.resources.inter
import com.lumbre.hotel.resources.playfair
import org.jetbrains.compose.resources.Font

// Paleta mediterránea compartida con la web: crema, arena, verde mar y dorado.
object Palette {
    val Cream = Color(0xFFFBF7F0)
    val Sand = Color(0xFFF3EBDD)
    val SandDeep = Color(0xFFE7DCC8)
    val Ink = Color(0xFF1C2B30)
    val Muted = Color(0xFF586669)
    val Sea = Color(0xFF0F5F66)
    val SeaDeep = Color(0xFF0B4A50)
    val SeaNight = Color(0xFF0C3A3F)
    val SeaSoft = Color(0xFFDCEEEC)
    val Gold = Color(0xFFA9762A)
    val GoldLight = Color(0xFFE9B95C)
    val GoldSoft = Color(0xFFF6E3C0)
    val Coral = Color(0xFFF2704F)
    val Turquoise = Color(0xFF0A7C86)
    val Sun = Color(0xFFF5A83A)
    val Navy = Color(0xFF16313A)
    val Sky = Color(0xFFE6F6FA)
    val SandLight = Color(0xFFFFF4E2)
    val Ok = Color(0xFF1F7A4D)
    val Error = Color(0xFFB3261E)
}

// Tema claro (predeterminado): blanco luminoso, turquesa de mar, sol, coral de atardecer y arena.
private val LightColors = lightColorScheme(
    primary = Palette.Turquoise, onPrimary = Color.White,
    primaryContainer = Color(0xFFD6F3F2), onPrimaryContainer = Color(0xFF00363B),
    secondary = Palette.Sun, onSecondary = Color(0xFF3A2400),
    secondaryContainer = Color(0xFFFFE9C7), onSecondaryContainer = Color(0xFF3A2400),
    tertiary = Palette.Coral, onTertiary = Color.White,
    tertiaryContainer = Color(0xFFFFDDD3), onTertiaryContainer = Color(0xFF3A0B00),
    background = Color.White, onBackground = Palette.Navy,
    surface = Color.White, onSurface = Palette.Navy,
    surfaceVariant = Color(0xFFF1F6F6), onSurfaceVariant = Color(0xFF5B6E73),
    surfaceContainerLowest = Color.White, surfaceContainerLow = Color(0xFFFBF9F5),
    surfaceContainer = Color(0xFFF6F1E8), surfaceContainerHigh = Color(0xFFF0E9DC), surfaceContainerHighest = Color(0xFFE9E0CF),
    outline = Color(0xFFB9C3C4), outlineVariant = Color(0xFFE3E8E8),
    error = Palette.Error, onError = Color.White, errorContainer = Color(0xFFFFDAD6), onErrorContainer = Color(0xFF410002),
    inverseSurface = Palette.SeaNight, inverseOnSurface = Color.White, inversePrimary = Color(0xFF7FD8D4),
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF7FC8C4), onPrimary = Color(0xFF003739),
    primaryContainer = Palette.Sea, onPrimaryContainer = Color(0xFFCFEDEA),
    secondary = Palette.GoldLight, onSecondary = Color(0xFF3D2A0A),
    secondaryContainer = Color(0xFF5A4013), onSecondaryContainer = Palette.GoldSoft,
    tertiary = Color(0xFFFFB59C), onTertiary = Color(0xFF5C1900),
    background = Color(0xFF0E1A1C), onBackground = Color(0xFFECE4D6),
    surface = Color(0xFF0E1A1C), onSurface = Color(0xFFECE4D6),
    surfaceVariant = Color(0xFF243336), onSurfaceVariant = Color(0xFFB9C6C4),
    surfaceContainerLowest = Color(0xFF0A1416), surfaceContainerLow = Color(0xFF132224),
    surfaceContainer = Color(0xFF172729), surfaceContainerHigh = Color(0xFF1F2F32), surfaceContainerHighest = Color(0xFF29393C),
    outline = Color(0xFF7D8B89), outlineVariant = Color(0xFF34474A),
    error = Color(0xFFFFB4AB), onError = Color(0xFF690005),
)

/** Colores semánticos que Material no cubre. */
@Immutable
data class Extras(val ok: Color, val okContainer: Color, val gold: Color, val heroScrim: Color, val sky: Color, val sand: Color, val glass: Color)

val LocalExtras = staticCompositionLocalOf {
    Extras(Palette.Ok, Color(0xFFD8F0E1), Color(0xFFB87A1E), Palette.SeaNight, Palette.Sky, Palette.SandLight, Color(0xE6FFFFFF))
}

@Composable
fun LumbreTheme(dark: Boolean, content: @Composable () -> Unit) {
    val sans = FontFamily(
        Font(Res.font.inter, FontWeight.Normal),
        Font(Res.font.inter, FontWeight.Medium),
        Font(Res.font.inter, FontWeight.SemiBold),
        Font(Res.font.inter, FontWeight.Bold),
    )
    val serif = FontFamily(
        Font(Res.font.playfair, FontWeight.Normal),
        Font(Res.font.playfair, FontWeight.SemiBold),
        Font(Res.font.playfair, FontWeight.Bold),
    )
    val b = Typography()
    fun TextStyle.display(w: FontWeight = FontWeight.SemiBold) = copy(fontFamily = serif, fontWeight = w, letterSpacing = 0.sp)
    fun TextStyle.text(w: FontWeight? = null) = copy(fontFamily = sans, fontWeight = w ?: fontWeight)
    val typography = Typography(
        displayLarge = b.displayLarge.display(), displayMedium = b.displayMedium.display(), displaySmall = b.displaySmall.display(),
        headlineLarge = b.headlineLarge.display(), headlineMedium = b.headlineMedium.display(), headlineSmall = b.headlineSmall.display(),
        titleLarge = b.titleLarge.text(FontWeight.SemiBold), titleMedium = b.titleMedium.text(FontWeight.SemiBold), titleSmall = b.titleSmall.text(FontWeight.SemiBold),
        bodyLarge = b.bodyLarge.text(), bodyMedium = b.bodyMedium.text(), bodySmall = b.bodySmall.text(),
        labelLarge = b.labelLarge.text(FontWeight.SemiBold), labelMedium = b.labelMedium.text(FontWeight.SemiBold), labelSmall = b.labelSmall.text(FontWeight.SemiBold),
    )
    val extras = if (dark) Extras(Color(0xFF8FD6AE), Color(0xFF15402A), Palette.GoldLight, Color(0xFF061416), Color(0xFF12262A), Color(0xFF1F2A2C), Color(0xCC132224))
    else Extras(Palette.Ok, Color(0xFFD8F0E1), Color(0xFFB87A1E), Palette.SeaNight, Palette.Sky, Palette.SandLight, Color(0xE6FFFFFF))

    androidx.compose.runtime.CompositionLocalProvider(LocalExtras provides extras) {
        MaterialTheme(
            colorScheme = if (dark) DarkColors else LightColors,
            typography = typography,
            shapes = Shapes(
                extraSmall = RoundedCornerShape(8.dp),
                small = RoundedCornerShape(12.dp),
                medium = RoundedCornerShape(20.dp),
                large = RoundedCornerShape(28.dp),
                extraLarge = RoundedCornerShape(36.dp),
            ),
            content = content,
        )
    }
}
