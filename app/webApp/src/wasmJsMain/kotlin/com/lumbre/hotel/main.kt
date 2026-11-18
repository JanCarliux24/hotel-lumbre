package com.lumbre.hotel

import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.window.ComposeViewport

private fun hideSplash(): Unit = js("{ const s = document.getElementById('splash'); if (s) { s.classList.add('out'); setTimeout(() => s.remove(), 500); } }")

@OptIn(ExperimentalComposeUiApi::class)
fun main() {
    ComposeViewport(viewportContainerId = "composeTarget") {
        App()
    }
    hideSplash()
}
