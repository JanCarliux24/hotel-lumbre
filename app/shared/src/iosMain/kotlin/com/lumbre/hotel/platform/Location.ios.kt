package com.lumbre.hotel.platform

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState

/**
 * iOS: por ahora se usa la región configurada en el iPhone (NSLocale), que no requiere permiso.
 * Para usar el GPS hay que añadir NSLocationWhenInUseUsageDescription en Info.plist e implementar
 * CLLocationManager; se deja como mejora porque no puede compilarse ni probarse fuera de macOS.
 */
@Composable
actual fun rememberLocationRequester(onResult: (LocationResult) -> Unit): () -> Unit {
    val callback = rememberUpdatedState(onResult)
    return remember { { callback.value(LocationResult.Unavailable) } }
}
