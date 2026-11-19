package com.lumbre.hotel.platform

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat

@Composable
actual fun rememberLocationRequester(onResult: (LocationResult) -> Unit): () -> Unit {
    val context = LocalContext.current
    val callback = rememberUpdatedState(onResult)
    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) readLocation(context) { callback.value(it) } else callback.value(LocationResult.Denied)
    }
    return remember(launcher) {
        {
            if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                readLocation(context) { callback.value(it) }
            } else {
                launcher.launch(Manifest.permission.ACCESS_COARSE_LOCATION)
            }
        }
    }
}

@SuppressLint("MissingPermission")
private fun readLocation(context: Context, done: (LocationResult) -> Unit) {
    val lm = context.getSystemService(Context.LOCATION_SERVICE) as? LocationManager ?: return done(LocationResult.Unavailable)
    val providers = listOf(LocationManager.NETWORK_PROVIDER, LocationManager.PASSIVE_PROVIDER, LocationManager.GPS_PROVIDER)
        .filter { runCatching { lm.isProviderEnabled(it) }.getOrDefault(false) }
    val last: Location? = providers.firstNotNullOfOrNull { runCatching { lm.getLastKnownLocation(it) }.getOrNull() }
    if (last != null) return done(LocationResult.Ok(last.latitude, last.longitude))
    val provider = providers.firstOrNull() ?: return done(LocationResult.Unavailable)
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
        lm.getCurrentLocation(provider, null, ContextCompat.getMainExecutor(context)) { loc ->
            done(if (loc != null) LocationResult.Ok(loc.latitude, loc.longitude) else LocationResult.Unavailable)
        }
    } else {
        done(LocationResult.Unavailable)
    }
}
