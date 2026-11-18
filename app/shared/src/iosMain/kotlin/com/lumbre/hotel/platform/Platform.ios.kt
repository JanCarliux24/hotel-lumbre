package com.lumbre.hotel.platform

import platform.Foundation.NSLocale
import platform.Foundation.currentLocale
import platform.Foundation.localeIdentifier

actual val platformKind: PlatformKind = PlatformKind.IOS

actual fun systemLanguageTag(): String = NSLocale.currentLocale.localeIdentifier.replace('_', '-')
