package com.lumbre.hotel.platform

/** Plataforma en la que se está ejecutando el código compartido. */
enum class PlatformKind { ANDROID, IOS, WEB }

/** Implementado en androidMain, iosMain y wasmJsMain. */
expect val platformKind: PlatformKind

/** Etiqueta de idioma del sistema o navegador, p. ej. "es-MX". */
expect fun systemLanguageTag(): String

/**
 * Normas de producto por plataforma y por rol. Toda la app comparte el mismo código, y estas
 * reglas deciden qué se ofrece en cada sitio (el servidor lo vuelve a comprobar con sus reglas):
 *
 * - Web: todo, según el rol (panel de administración para recepción y superiores; panel de
 *   superusuario solo para el superusuario). Es el puesto de trabajo de la oficina.
 * - Móvil: lo útil sobre la marcha: reservar, mis reservas, llave digital y, para el personal,
 *   la pantalla de recepción (llegadas y registro rápido). La gestión completa queda en la web.
 */
object Capabilities {
    val isWeb: Boolean get() = platformKind == PlatformKind.WEB
    val isMobile: Boolean get() = platformKind != PlatformKind.WEB

    /** La plataforma admite paneles de gestión (pantalla grande, teclado, puesto fijo). */
    val adminPanel: Boolean get() = isWeb
    val digitalKey: Boolean get() = isMobile

    fun reception(role: com.lumbre.hotel.data.Role) = role.atLeast(com.lumbre.hotel.data.Role.STAFF)
    fun admin(role: com.lumbre.hotel.data.Role) = isWeb && role.atLeast(com.lumbre.hotel.data.Role.STAFF)
    fun manageCatalog(role: com.lumbre.hotel.data.Role) = isWeb && role.atLeast(com.lumbre.hotel.data.Role.ADMIN)
    fun superPanel(role: com.lumbre.hotel.data.Role) = isWeb && role == com.lumbre.hotel.data.Role.SUPERADMIN
}
