package com.lumbre.hotel.platform

import java.util.Locale

actual val platformKind: PlatformKind = PlatformKind.ANDROID

actual fun systemLanguageTag(): String = Locale.getDefault().toLanguageTag()
