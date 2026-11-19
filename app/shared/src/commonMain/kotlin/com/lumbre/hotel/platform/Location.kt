package com.lumbre.hotel.platform

import androidx.compose.runtime.Composable
import com.lumbre.hotel.data.firebase.http
import io.ktor.client.call.body
import io.ktor.client.request.get
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.jsonPrimitive
import kotlin.math.roundToInt

/** Resultado de pedir la ubicación: coordenadas o el motivo por el que no se obtuvieron. */
sealed interface LocationResult {
    data class Ok(val lat: Double, val lon: Double) : LocationResult
    data object Denied : LocationResult
    data object Unavailable : LocationResult
}

/**
 * Devuelve una función que, al llamarla, pide permiso de ubicación aproximada al sistema
 * (Android: permiso en tiempo de ejecución; web: diálogo del navegador) y entrega el resultado.
 */
@Composable
expect fun rememberLocationRequester(onResult: (LocationResult) -> Unit): () -> Unit

/**
 * Obtiene el código de país a partir de coordenadas. Por privacidad se redondean a 1 decimal
 * (unos 11 km) antes de consultar el servicio gratuito de BigDataCloud; si falla, se usa una
 * aproximación local por zonas.
 */
suspend fun countryFromCoordinates(lat: Double, lon: Double): String? {
    val la = (lat * 10).roundToInt() / 10.0
    val lo = (lon * 10).roundToInt() / 10.0
    val remote = runCatching {
        val o: JsonObject = http.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=$la&longitude=$lo&localityLanguage=en").body()
        o["countryCode"]?.jsonPrimitive?.contentOrNull?.takeIf { it.length == 2 }
    }.getOrNull()
    return remote ?: roughCountry(la, lo)
}

/** Aproximación sin red para los países principales del hotel. */
internal fun roughCountry(lat: Double, lon: Double): String? = when {
    lat in 14.5..32.7 && lon in -118.4..-86.7 && !(lat > 31.3 && lon < -108.2) -> "MX"
    lat in 24.5..49.4 && lon in -125.0..-66.9 -> "US"
    lat in 49.0..60.0 && lon in -141.0..-52.0 -> "CA"
    lat in 35.9..43.8 && lon in -9.4..3.4 -> if (lon < -6.2 && lat > 36.9) "PT" else "ES"
    lat in 27.6..29.5 && lon in -18.2..-13.4 -> "ES"
    lat in 41.3..51.1 && lon in -5.2..9.6 -> "FR"
    lat in 49.9..58.7 && lon in -8.2..1.8 -> "GB"
    lat in -33.8..5.3 && lon in -73.99..-34.8 -> "BR"
    lat in -4.3..12.5 && lon in -79.0..-66.8 -> "CO"
    lat in -55.1..-21.7 && lon in -73.6..-53.6 -> "AR"
    else -> null
}
