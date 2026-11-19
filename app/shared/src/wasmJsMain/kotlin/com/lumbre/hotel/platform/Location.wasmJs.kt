package com.lumbre.hotel.platform

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState

private fun geolocate(ok: (Double, Double) -> Unit, err: (Int) -> Unit): Unit = js(
    """{
        if (!navigator.geolocation) { err(-1); return; }
        navigator.geolocation.getCurrentPosition(
            (p) => ok(p.coords.latitude, p.coords.longitude),
            (e) => err(e.code),
            { enableHighAccuracy: false, timeout: 12000, maximumAge: 600000 }
        );
    }"""
)

/** En el navegador se usa la API de geolocalización: el navegador muestra su propio diálogo de permiso. */
@Composable
actual fun rememberLocationRequester(onResult: (LocationResult) -> Unit): () -> Unit {
    val callback = rememberUpdatedState(onResult)
    return remember {
        {
            geolocate(
                { lat, lon -> callback.value(LocationResult.Ok(lat, lon)) },
                { code -> callback.value(if (code == 1) LocationResult.Denied else LocationResult.Unavailable) },
            )
        }
    }
}
