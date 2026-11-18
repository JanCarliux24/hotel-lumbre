package com.lumbre.hotel.platform

/** Plataforma en la que se está ejecutando el código compartido. */
enum class PlatformKind { ANDROID, IOS, WEB }

/** Implementado en androidMain, iosMain y wasmJsMain. */
expect val platformKind: PlatformKind

/** Etiqueta de idioma del sistema o navegador, p. ej. "es-MX". */
expect fun systemLanguageTag(): String

/**
 * Normas de producto por plataforma. Toda la app comparte el mismo código, y estas
 * banderas deciden qué funciones se ofrecen en cada sitio:
 *
 * - El panel administrativo solo existe en la web: requiere pantalla grande, teclado
 *   y un entorno de trabajo controlado (recepción u oficina), no un móvil personal.
 * - La llave digital solo existe en móvil: depende de llevar el dispositivo encima
 *   (NFC/Bluetooth junto a la cerradura) y de la vibración háptica.
 */
object Capabilities {
    val adminPanel: Boolean get() = platformKind == PlatformKind.WEB
    val digitalKey: Boolean get() = platformKind != PlatformKind.WEB
    val isMobile: Boolean get() = platformKind != PlatformKind.WEB
}
