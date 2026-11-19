package com.lumbre.hotel.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Cookie
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.MyLocation
import androidx.compose.material.icons.rounded.Shield
import androidx.compose.material.icons.rounded.Tune
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.data.Consent
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.regionName
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.i18n.tr
import com.lumbre.hotel.platform.LocationResult
import com.lumbre.hotel.platform.countryFromCoordinates
import com.lumbre.hotel.platform.rememberLocationRequester
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.FloatingIcon
import com.lumbre.hotel.ui.components.LocalSnackbar
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.theme.LocalExtras
import kotlinx.coroutines.launch

/**
 * Detecta el país por ubicación (si el usuario lo permite) y aplica idioma y moneda.
 * Devuelve la función que lanza la petición y el estado "buscando".
 */
@Composable
fun rememberLocateAndApply(): Pair<() -> Unit, Boolean> {
    val repo = AppGraph.repo
    val scope = rememberCoroutineScope()
    val snackbar = LocalSnackbar.current
    var busy by remember { mutableStateOf(false) }
    val lang = LocalLang.current
    val request = rememberLocationRequester { result ->
        when (result) {
            is LocationResult.Ok -> scope.launch {
                val cc = countryFromCoordinates(result.lat, result.lon)
                busy = false
                if (cc != null) {
                    repo.applyCountry(cc)
                    val newLang = repo.prefs.value.lang
                    snackbar.showSnackbar(tr(newLang, K.LOC_OK, regionName(cc, newLang) ?: cc))
                } else snackbar.showSnackbar(tr(lang, K.LOC_UNAVAILABLE))
            }
            LocationResult.Denied -> { busy = false; scope.launch { snackbar.showSnackbar(tr(lang, K.LOC_DENIED)) } }
            LocationResult.Unavailable -> { busy = false; scope.launch { snackbar.showSnackbar(tr(lang, K.LOC_UNAVAILABLE)) } }
        }
    }
    return Pair({ busy = true; request() }, busy)
}

@Composable
fun PrivacyScreen() {
    val repo = AppGraph.repo
    val prefs by repo.prefs.collectAsState()
    val consent = prefs.consent
    var preferences by remember(consent) { mutableStateOf(consent.preferences) }
    var location by remember(consent) { mutableStateOf(consent.location) }
    val (locate, busy) = rememberLocateAndApply()

    MaxWidth(Modifier.fillMaxSize(), max = 820.dp) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).statusBarsPadding().padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.appear(0)) {
                Column(Modifier.weight(1f)) {
                    Text(t(K.PRIV_TITLE), style = MaterialTheme.typography.displaySmall)
                    Spacer(Modifier.height(6.dp))
                    Text(t(K.PRIV_SUB), style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                FloatingIcon(Icons.Rounded.Cookie, MaterialTheme.colorScheme.secondary, size = 44.dp)
            }
            Spacer(Modifier.height(20.dp))
            PrivacyCard(1) {
                ConsentRow(Icons.Rounded.Lock, t(K.CK_NECESSARY), t(K.CK_NECESSARY_D), checked = true, enabled = false) {}
                ConsentRow(Icons.Rounded.Tune, t(K.CK_PREFS), t(K.CK_PREFS_D), preferences) { preferences = it }
                ConsentRow(Icons.Rounded.MyLocation, t(K.CK_LOCATION), t(K.CK_LOCATION_D), location) { location = it }
                Spacer(Modifier.height(12.dp))
                FlowRow(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    LumbreButton(t(K.CK_SAVE), { repo.setConsent(Consent(preferences = preferences, location = location)) })
                    LumbreButton(t(K.CK_ACCEPT_ALL), { preferences = true; location = true; repo.setConsent(Consent(preferences = true, location = true)) }, kind = BtnKind.Secondary)
                    LumbreButton(t(K.CK_ONLY_NEEDED), { preferences = false; location = false; repo.setConsent(Consent()) }, kind = BtnKind.Secondary)
                }
                if (consent.decided) {
                    Spacer(Modifier.height(10.dp))
                    Text(
                        "${t(K.PRIV_CURRENT)}: " + listOfNotNull(
                            t(K.CK_NECESSARY),
                            t(K.CK_PREFS).takeIf { consent.preferences },
                            t(K.CK_LOCATION).takeIf { consent.location },
                        ).joinToString(" · "),
                        style = MaterialTheme.typography.bodySmall, color = LocalExtras.current.ok,
                    )
                }
            }
            PrivacyCard(2) {
                Text(t(K.CK_LOCATION), style = MaterialTheme.typography.titleLarge)
                Spacer(Modifier.height(6.dp))
                Text(t(K.CK_LOCATION_D), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(14.dp))
                if (busy) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        CircularProgressIndicator(Modifier.size(22.dp), strokeWidth = 2.dp)
                        Spacer(Modifier.width(10.dp)); Text(t(K.LOC_DETECTING))
                    }
                } else {
                    LumbreButton(t(K.LOC_BUTTON), locate, Modifier.fillMaxWidth(), enabled = consent.location, icon = Icons.Rounded.MyLocation)
                    if (!consent.location) Text(t(K.LOC_NEED_CONSENT), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(top = 8.dp))
                }
                Spacer(Modifier.height(10.dp))
                Text(regionName(prefs.region, prefs.lang)?.let { t(K.REGION, it) } ?: t(K.REGION_UNKNOWN), style = MaterialTheme.typography.bodySmall)
            }
            PrivacyCard(3) {
                Text(t(K.PRIV_DATA_TITLE), style = MaterialTheme.typography.titleLarge)
                Spacer(Modifier.height(8.dp))
                listOf(K.PRIV_D1, K.PRIV_D2, K.PRIV_D3, K.PRIV_D4).forEach {
                    Row(Modifier.padding(vertical = 6.dp)) {
                        Icon(Icons.Rounded.Shield, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
                        Spacer(Modifier.width(10.dp))
                        Text(t(it), style = MaterialTheme.typography.bodyMedium)
                    }
                }
                Spacer(Modifier.height(10.dp))
                Text(t(K.PRIV_RIGHTS), style = MaterialTheme.typography.titleMedium)
                Text(t(K.PRIV_RIGHTS_D), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
private fun PrivacyCard(index: Int, content: @Composable () -> Unit) {
    Card(
        Modifier.fillMaxWidth().padding(bottom = 16.dp).appear(index),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
    ) { Column(Modifier.padding(20.dp)) { content() } }
}

@Composable
private fun ConsentRow(icon: ImageVector, title: String, sub: String, checked: Boolean, enabled: Boolean = true, onChange: (Boolean) -> Unit) {
    Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, tint = MaterialTheme.colorScheme.primary)
        Spacer(Modifier.width(12.dp))
        Column(Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(sub, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Spacer(Modifier.width(10.dp))
        Switch(checked = checked, onCheckedChange = onChange, enabled = enabled)
    }
}

/** Aviso inicial de cookies y ubicación (una sola vez, hasta que el usuario decide). */
@Composable
fun ConsentBanner(onConfigure: () -> Unit, modifier: Modifier = Modifier) {
    val repo = AppGraph.repo
    val prefs by repo.prefs.collectAsState()
    val (locate, _) = rememberLocateAndApply()
    AnimatedVisibility(
        visible = !prefs.consent.decided,
        enter = slideInVertically { it } + fadeIn(), exit = slideOutVertically { it } + fadeOut(),
        modifier = modifier,
    ) {
        Box(Modifier.fillMaxWidth().navigationBarsPadding().padding(16.dp), contentAlignment = Alignment.BottomCenter) {
            Card(
                Modifier.widthIn(max = 640.dp).fillMaxWidth(),
                shape = RoundedCornerShape(28.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
                elevation = CardDefaults.cardElevation(18.dp),
            ) {
                Column(Modifier.padding(22.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        FloatingIcon(Icons.Rounded.Cookie, MaterialTheme.colorScheme.secondary, size = 28.dp)
                        Spacer(Modifier.width(10.dp))
                        Text(t(K.CK_BANNER_TITLE), style = MaterialTheme.typography.titleLarge)
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(t(K.CK_BANNER_TEXT), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(16.dp))
                    FlowRow(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        LumbreButton(t(K.CK_ACCEPT_ALL), {
                            repo.setConsent(Consent(preferences = true, location = true)); locate()
                        }, icon = Icons.Rounded.MyLocation)
                        LumbreButton(t(K.CK_ONLY_NEEDED), { repo.setConsent(Consent()) }, kind = BtnKind.Secondary)
                        LumbreButton(t(K.CK_CONFIGURE), onConfigure, kind = BtnKind.Secondary)
                    }
                }
            }
        }
    }
}
