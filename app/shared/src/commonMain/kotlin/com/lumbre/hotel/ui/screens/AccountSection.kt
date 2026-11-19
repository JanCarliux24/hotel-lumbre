package com.lumbre.hotel.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.CloudDone
import androidx.compose.material.icons.rounded.Email
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.Logout
import androidx.compose.material.icons.rounded.MarkEmailRead
import androidx.compose.material.icons.rounded.Visibility
import androidx.compose.material.icons.rounded.VisibilityOff
import androidx.compose.material.icons.rounded.WarningAmber
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.lumbre.hotel.data.Account
import com.lumbre.hotel.data.AppGraph
import com.lumbre.hotel.domain.Validation
import com.lumbre.hotel.i18n.K
import com.lumbre.hotel.i18n.LocalLang
import com.lumbre.hotel.i18n.t
import com.lumbre.hotel.i18n.tr
import com.lumbre.hotel.ui.components.BtnKind
import com.lumbre.hotel.ui.components.LocalSnackbar
import com.lumbre.hotel.ui.components.LumbreButton
import com.lumbre.hotel.ui.theme.LocalExtras
import com.lumbre.hotel.ui.theme.Palette
import kotlinx.coroutines.launch

/** Tarjeta de cuenta: formularios de acceso o, con sesión, datos y seguridad. */
@Composable
fun AccountSection() {
    val repo = AppGraph.repo
    val account by repo.account.collectAsState()
    val syncing by repo.syncing.collectAsState()
    AnimatedContent(account, transitionSpec = { fadeIn() togetherWith fadeOut() }, label = "acc") { acc ->
        if (acc == null) AuthForms() else SignedIn(acc, syncing)
    }
}

@Composable
private fun AuthForms() {
    val repo = AppGraph.repo
    val params by repo.params.collectAsState()
    val scope = rememberCoroutineScope()
    val snackbar = LocalSnackbar.current
    val lang = LocalLang.current
    var mode by remember { mutableStateOf(0) } // 0 = entrar, 1 = crear cuenta
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var pass by remember { mutableStateOf("") }
    var pass2 by remember { mutableStateOf("") }
    var terms by remember { mutableStateOf(false) }
    var tried by remember { mutableStateOf(false) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<K?>(null) }

    val nameErr = if (mode == 1) Validation.name(name) else null
    val emailErr = Validation.email(email)
    val phoneErr = if (mode == 1) Validation.phone(phone) else null
    val passErr = if (mode == 1) Validation.password(pass, params.minPasswordLength, email) else if (pass.isEmpty()) K.E_REQUIRED else null
    val pass2Err = if (mode == 1) Validation.passwordsMatch(pass, pass2) else null
    val termsErr = if (mode == 1 && !terms) K.E_TERMS else null

    Column {
        Text(t(K.ACC_SIGNIN_SUB), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Spacer(Modifier.height(14.dp))
        SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth()) {
            listOf(K.ACC_SIGNIN, K.ACC_SIGNUP).forEachIndexed { i, k ->
                SegmentedButton(selected = mode == i, onClick = { mode = i; tried = false; error = null }, shape = SegmentedButtonDefaults.itemShape(i, 2)) { Text(t(k)) }
            }
        }
        Spacer(Modifier.height(12.dp))
        AnimatedVisibility(mode == 1) {
            Column {
                Field(name, { name = it.take(80) }, t(K.NAME), if (tried) nameErr else null,
                    KeyboardOptions(capitalization = KeyboardCapitalization.Words, imeAction = ImeAction.Next))
                Field(phone, { v -> phone = v.filter { it.isDigit() || it in "+ ().-" }.take(22) }, t(K.PHONE) + " · " + t(K.PHONE_HINT), if (tried) phoneErr else null,
                    KeyboardOptions(keyboardType = KeyboardType.Phone, imeAction = ImeAction.Next))
            }
        }
        Field(email, { email = it.trim().take(254) }, t(K.EMAIL), if (tried) emailErr else null,
            KeyboardOptions(keyboardType = KeyboardType.Email, imeAction = ImeAction.Next), leading = { Icon(Icons.Rounded.Email, null) })
        PasswordField(pass, { pass = it.take(128) }, t(K.ACC_PASSWORD), if (tried) passErr else null)
        if (mode == 1) {
            StrengthMeter(pass)
            Text(t(K.PASS_HINT, params.minPasswordLength), style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Spacer(Modifier.height(6.dp))
            PasswordField(pass2, { pass2 = it.take(128) }, t(K.ACC_PASSWORD2), if (tried) pass2Err else null)
            Row(verticalAlignment = Alignment.CenterVertically) {
                Checkbox(terms, { terms = it })
                Text(t(K.ACC_TERMS), style = MaterialTheme.typography.bodyMedium,
                    color = if (tried && termsErr != null) MaterialTheme.colorScheme.error else Color.Unspecified)
            }
        }
        error?.let {
            val msg = if (it == K.E_LOCKED) t(it, repo.lockoutRemainingSec()) else t(it)
            Row(Modifier.padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Rounded.WarningAmber, null, tint = MaterialTheme.colorScheme.error, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(6.dp)); Text(msg, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyMedium)
            }
        }
        Spacer(Modifier.height(8.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            LumbreButton(if (mode == 0) t(K.ACC_SIGNIN) else t(K.ACC_SIGNUP), enabled = !busy, modifier = Modifier.weight(1f), onClick = {
                tried = true
                val errs = listOf(nameErr, emailErr, phoneErr, passErr, pass2Err, termsErr)
                if (errs.any { it != null }) return@LumbreButton
                busy = true; error = null
                scope.launch {
                    error = if (mode == 0) repo.login(email, pass) else repo.register(name, email, phone, pass)
                    busy = false
                    if (error == null) { pass = ""; pass2 = "" }
                }
            })
            if (busy) { Spacer(Modifier.width(12.dp)); CircularProgressIndicator(Modifier.size(24.dp), strokeWidth = 2.dp) }
        }
        if (mode == 0) TextButton(onClick = {
            if (Validation.email(email) != null) { tried = true; return@TextButton }
            scope.launch { repo.resetPassword(email); snackbar.showSnackbar(tr(lang, K.ACC_RESET_SENT)) }
        }) { Text(t(K.ACC_FORGOT)) }
    }
}

@Composable
private fun SignedIn(acc: Account, syncing: Boolean) {
    val repo = AppGraph.repo
    val params by repo.params.collectAsState()
    val scope = rememberCoroutineScope()
    val snackbar = LocalSnackbar.current
    val lang = LocalLang.current
    var name by remember(acc) { mutableStateOf(acc.name) }
    var phone by remember(acc) { mutableStateOf(acc.phone) }
    var newPass by remember { mutableStateOf("") }
    var showDelete by remember { mutableStateOf(false) }
    val ex = LocalExtras.current

    Column {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(Modifier.size(52.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primaryContainer), contentAlignment = Alignment.Center) {
                Text(acc.name.split(' ').mapNotNull { it.firstOrNull()?.uppercase() }.take(2).joinToString("").ifBlank { "·" },
                    style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onPrimaryContainer)
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text(t(K.ACC_HELLO, acc.name.substringBefore(' ').ifBlank { acc.email }), style = MaterialTheme.typography.titleLarge)
                Text(acc.email, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Text(t(roleKey(acc.role)), style = MaterialTheme.typography.labelLarge, color = Palette.Navy,
                modifier = Modifier.clip(RoundedCornerShape(50)).background(Palette.SandLight).padding(horizontal = 12.dp, vertical = 6.dp))
        }
        Spacer(Modifier.height(10.dp))
        FlowRow(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Chip(Icons.Rounded.CloudDone, if (syncing) t(K.SYNCING) else t(K.ACC_SYNC), ex.ok)
            if (acc.emailVerified) Chip(Icons.Rounded.MarkEmailRead, t(K.ACC_VERIFIED), ex.ok)
            else {
                Chip(Icons.Rounded.WarningAmber, t(K.ACC_NOT_VERIFIED), MaterialTheme.colorScheme.error)
                TextButton(onClick = { scope.launch { repo.resendVerification(); snackbar.showSnackbar(tr(lang, K.ACC_VERIFY_SENT)) } }) { Text(t(K.ACC_RESEND)) }
            }
        }
        Spacer(Modifier.height(16.dp))
        Text(t(K.ACC_PROFILE), style = MaterialTheme.typography.titleMedium)
        val nameErr = Validation.name(name); val phoneErr = Validation.phone(phone)
        Field(name, { name = it.take(80) }, t(K.NAME), nameErr, KeyboardOptions(capitalization = KeyboardCapitalization.Words))
        Field(phone, { v -> phone = v.filter { it.isDigit() || it in "+ ().-" }.take(22) }, t(K.PHONE), phoneErr, KeyboardOptions(keyboardType = KeyboardType.Phone))
        LumbreButton(t(K.SAVE), kind = BtnKind.Secondary, enabled = nameErr == null && phoneErr == null && (name != acc.name || phone != acc.phone), onClick = {
            scope.launch { val e = repo.updateProfile(name, phone); snackbar.showSnackbar(tr(lang, e ?: K.ACC_SAVED)) }
        })
        Spacer(Modifier.height(18.dp))
        Text(t(K.ACC_SECURITY), style = MaterialTheme.typography.titleMedium)
        val passErr = if (newPass.isEmpty()) null else Validation.password(newPass, params.minPasswordLength, acc.email)
        PasswordField(newPass, { newPass = it.take(128) }, t(K.ACC_NEW_PASS), passErr)
        if (newPass.isNotEmpty()) StrengthMeter(newPass)
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            LumbreButton(t(K.ACC_CHANGE_PASS), kind = BtnKind.Secondary, icon = Icons.Rounded.Lock, enabled = newPass.isNotEmpty() && passErr == null, onClick = {
                scope.launch { val e = repo.changePassword(newPass); if (e == null) newPass = ""; snackbar.showSnackbar(tr(lang, e ?: K.ACC_PASS_CHANGED)) }
            })
            LumbreButton(t(K.ACC_SIGNOUT), { repo.logout() }, kind = BtnKind.Secondary, icon = Icons.Rounded.Logout)
        }
        TextButton(onClick = { showDelete = true }) { Text(t(K.ACC_DELETE), color = MaterialTheme.colorScheme.error) }
    }

    if (showDelete) AlertDialog(
        onDismissRequest = { showDelete = false },
        title = { Text(t(K.ACC_DELETE)) }, text = { Text(t(K.ACC_DELETE_Q)) },
        confirmButton = { TextButton(onClick = { showDelete = false; scope.launch { repo.deleteAccount()?.let { snackbar.showSnackbar(tr(lang, it)) } } }) { Text(t(K.DELETE), color = MaterialTheme.colorScheme.error) } },
        dismissButton = { TextButton(onClick = { showDelete = false }) { Text(t(K.CANCEL)) } },
    )
}

@Composable
private fun Chip(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String, color: Color) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 4.dp)) {
        Icon(icon, null, tint = color, modifier = Modifier.size(18.dp)); Spacer(Modifier.width(6.dp))
        Text(text, style = MaterialTheme.typography.bodySmall, color = color)
    }
}

@Composable
private fun Field(
    value: String, onChange: (String) -> Unit, label: String, error: K?,
    keyboard: KeyboardOptions = KeyboardOptions.Default, leading: (@Composable () -> Unit)? = null,
) {
    OutlinedTextField(
        value, onChange, label = { Text(label) }, singleLine = true, isError = error != null,
        supportingText = error?.let { { Text(t(it)) } }, keyboardOptions = keyboard, leadingIcon = leading,
        shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 4.dp),
    )
}

@Composable
private fun PasswordField(value: String, onChange: (String) -> Unit, label: String, error: K?) {
    var show by remember { mutableStateOf(false) }
    val params by AppGraph.repo.params.collectAsState()
    OutlinedTextField(
        value, onChange, label = { Text(label) }, singleLine = true, isError = error != null,
        supportingText = error?.let { { Text(if (it == K.E_PASS_LENGTH) t(it, params.minPasswordLength) else t(it)) } },
        visualTransformation = if (show) VisualTransformation.None else PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password, imeAction = ImeAction.Done),
        leadingIcon = { Icon(Icons.Rounded.Lock, null) },
        trailingIcon = { IconButton(onClick = { show = !show }) { Icon(if (show) Icons.Rounded.VisibilityOff else Icons.Rounded.Visibility, t(K.ACC_SHOW)) } },
        shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 4.dp),
    )
}

/** Medidor animado de fuerza de la contraseña. */
@Composable
fun StrengthMeter(password: String) {
    val score = Validation.passwordStrength(password)
    val fill by animateFloatAsState((score + 1) / 5f, spring(dampingRatio = 0.6f), label = "strength")
    val color by animateColorAsState(
        when (score) { 0, 1 -> MaterialTheme.colorScheme.error; 2 -> Palette.Sun; else -> LocalExtras.current.ok }, label = "strengthColor",
    )
    Column(Modifier.padding(vertical = 4.dp)) {
        Box(Modifier.fillMaxWidth().height(8.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceContainerHigh)) {
            Box(Modifier.fillMaxWidth(fill).height(8.dp).clip(CircleShape).background(color))
        }
        Text(t(listOf(K.STRENGTH_0, K.STRENGTH_1, K.STRENGTH_2, K.STRENGTH_3, K.STRENGTH_4)[score]),
            style = MaterialTheme.typography.labelMedium, color = color, modifier = Modifier.padding(top = 4.dp))
    }
}
