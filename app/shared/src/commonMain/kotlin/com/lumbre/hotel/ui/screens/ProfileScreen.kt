package com.lumbre.hotel.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.KeyboardArrowRight
import androidx.compose.material.icons.rounded.AdminPanelSettings
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.DeleteOutline
import androidx.compose.material.icons.rounded.Devices
import androidx.compose.material.icons.rounded.Laptop
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.Smartphone
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.regionName
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.platform.Capabilities
import com.lumbre.hotel.platform.PlatformKind
import com.lumbre.hotel.platform.platformKind
import com.lumbre.hotel.ui.components.Lumi
import com.lumbre.hotel.ui.components.MaxWidth
import com.lumbre.hotel.ui.components.Mood
import com.lumbre.hotel.ui.components.appear
import com.lumbre.hotel.ui.components.bounceClick
import com.lumbre.hotel.ui.theme.LocalExtras

@Composable
fun ProfileScreen(onOpenAdmin: () -> Unit) {
    val repo = AppGraph.repo
    val prefs by repo.prefs.collectAsState()
    val all by repo.reservations.collectAsState()
    val name = all.firstOrNull { it.mine }?.guestName ?: t(K.GUEST)
    var adminInfo by remember { mutableStateOf(false) }
    var confirmClear by remember { mutableStateOf(false) }

    MaxWidth(Modifier.fillMaxSize(), max = 760.dp) {
        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).statusBarsPadding().padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.appear(0)) {
                Box(Modifier.size(64.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primaryContainer), contentAlignment = Alignment.Center) {
                    Text(name.split(' ').mapNotNull { it.firstOrNull()?.uppercase() }.take(2).joinToString(""), style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.onPrimaryContainer)
                }
                Spacer(Modifier.width(16.dp))
                Column(Modifier.weight(1f)) {
                    Text(t(K.PROFILE_TITLE), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(name, style = MaterialTheme.typography.headlineSmall)
                }
                Lumi(Mood.Happy, Unit, Modifier.size(60.dp))
            }

            Section(t(K.PREFS), 1) {
                LanguageSelector(prefs.lang) { repo.setLang(it) }
                Spacer(Modifier.height(18.dp))
                CurrencySelector(prefs.currency) { repo.setCurrency(it) }
                Spacer(Modifier.height(12.dp))
                Text(
                    regionName(prefs.region, prefs.lang)?.let { t(K.REGION, it) } ?: t(K.REGION_UNKNOWN),
                    style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            // Qué se puede hacer en esta plataforma: mismas reglas en todo el código (Capabilities).
            Section(t(K.CAPS_TITLE), 2) {
                val (pIcon, pLabel) = when (platformKind) {
                    PlatformKind.ANDROID -> Icons.Rounded.Smartphone to K.PL_ANDROID
                    PlatformKind.IOS -> Icons.Rounded.Smartphone to K.PL_IOS
                    PlatformKind.WEB -> Icons.Rounded.Laptop to K.PL_WEB
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(pIcon, null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(10.dp))
                    Text("${t(K.PLATFORM_TITLE)}: ", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(t(pLabel), style = MaterialTheme.typography.titleSmall)
                }
                Spacer(Modifier.height(12.dp))
                CapRow(K.CAP_BOOK, true)
                CapRow(K.CAP_KEY, Capabilities.digitalKey)
                CapRow(K.CAP_ADMIN, Capabilities.adminPanel)
                CapRow(K.CAP_SYNC, true, Icons.Rounded.Devices)
            }

            Section(t(K.ADMIN_WEB_ONLY), 3) {
                if (Capabilities.adminPanel) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Rounded.AdminPanelSettings, null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(12.dp))
                        Column(Modifier.weight(1f)) {
                            Text(t(K.ADMIN_MODE), style = MaterialTheme.typography.titleMedium)
                            Text(t(K.ADMIN_MODE_SUB), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Switch(checked = prefs.admin, onCheckedChange = { repo.setAdmin(it); if (it) onOpenAdmin() })
                    }
                } else {
                    // En móvil la opción se ve pero está bloqueada, con explicación.
                    Row(
                        Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).bounceClick(scaleDown = 0.98f) { adminInfo = true }.padding(vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Icon(Icons.Rounded.Lock, null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.width(12.dp))
                        Column(Modifier.weight(1f)) {
                            Text(t(K.ADMIN_WEB_ONLY), style = MaterialTheme.typography.titleMedium)
                            Text(t(K.ADMIN_WEB_ONLY_SUB), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Icon(Icons.AutoMirrored.Rounded.KeyboardArrowRight, null)
                    }
                }
            }

            Section(t(K.ABOUT_DATA), 4) {
                Row(
                    Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).bounceClick(scaleDown = 0.98f) { confirmClear = true }.padding(vertical = 6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Icon(Icons.Rounded.DeleteOutline, null, tint = MaterialTheme.colorScheme.error)
                    Spacer(Modifier.width(12.dp))
                    Text(t(K.CLEAR_DATA), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.error)
                }
            }
            Spacer(Modifier.height(24.dp))
        }
    }

    if (adminInfo) {
        AlertDialog(
            onDismissRequest = { adminInfo = false },
            icon = { Icon(Icons.Rounded.Laptop, null) },
            title = { Text(t(K.ADMIN_WEB_ONLY_SUB)) },
            text = { Text(t(K.ADMIN_WEB_ONLY_TEXT)) },
            confirmButton = { TextButton(onClick = { adminInfo = false }) { Text(t(K.CLOSE)) } },
        )
    }
    if (confirmClear) {
        AlertDialog(
            onDismissRequest = { confirmClear = false },
            title = { Text(t(K.CLEAR_DATA)) },
            text = { Text(t(K.CLEAR_DATA_Q)) },
            confirmButton = {
                TextButton(onClick = { repo.clearMyData(); confirmClear = false }) { Text(t(K.DELETE), color = MaterialTheme.colorScheme.error) }
            },
            dismissButton = { TextButton(onClick = { confirmClear = false }) { Text(t(K.CANCEL)) } },
        )
    }
}

@Composable
private fun Section(title: String, index: Int, content: @Composable () -> Unit) {
    Spacer(Modifier.height(20.dp))
    Card(
        Modifier.fillMaxWidth().appear(index),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceContainerLowest),
    ) {
        Column(Modifier.padding(20.dp)) {
            Text(title, style = MaterialTheme.typography.titleLarge)
            Spacer(Modifier.height(14.dp))
            content()
        }
    }
}

@Composable
private fun CapRow(label: K, available: Boolean, icon: ImageVector? = null) {
    Row(Modifier.padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(
            icon ?: if (available) Icons.Rounded.CheckCircle else Icons.Rounded.Lock, null,
            tint = if (available) LocalExtras.current.ok else MaterialTheme.colorScheme.outline,
            modifier = Modifier.size(20.dp),
        )
        Spacer(Modifier.width(10.dp))
        Text(t(label), style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
        Text(
            if (available) t(K.ONLY_HERE) else t(K.NOT_HERE),
            style = MaterialTheme.typography.labelMedium,
            color = if (available) LocalExtras.current.ok else MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
