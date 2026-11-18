package com.lumbre.hotel.platform

actual val platformKind: PlatformKind = PlatformKind.WEB

/**
 * Idioma del navegador. Si no trae país (p. ej. "es" a secas), se completa con la región
 * deducida de la zona horaria, sin pedir permisos de ubicación ni consultar servicios externos.
 */
private fun browserLanguageTag(): String = js(
    """(() => {
        const lang = navigator.language || 'es';
        if (lang.indexOf('-') > 0) return lang;
        let tz = '';
        try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
        const zones = {
            'Europe/Madrid': 'ES', 'Atlantic/Canary': 'ES', 'Europe/Paris': 'FR', 'Europe/Lisbon': 'PT', 'Europe/London': 'GB',
            'Europe/Dublin': 'IE', 'Europe/Brussels': 'BE', 'America/Mexico_City': 'MX', 'America/Monterrey': 'MX',
            'America/Tijuana': 'MX', 'America/Cancun': 'MX', 'America/Merida': 'MX', 'America/Chihuahua': 'MX',
            'America/Hermosillo': 'MX', 'America/Mazatlan': 'MX', 'America/Bogota': 'CO', 'America/Sao_Paulo': 'BR',
            'America/Bahia': 'BR', 'America/Fortaleza': 'BR', 'America/Manaus': 'BR', 'America/Recife': 'BR',
            'America/Argentina/Buenos_Aires': 'AR', 'America/Santiago': 'CL', 'America/Lima': 'PE',
            'America/New_York': 'US', 'America/Chicago': 'US', 'America/Denver': 'US', 'America/Los_Angeles': 'US',
            'America/Phoenix': 'US', 'Pacific/Honolulu': 'US', 'America/Toronto': 'CA', 'America/Vancouver': 'CA'
        };
        return zones[tz] ? lang + '-' + zones[tz] : lang;
    })()"""
)

actual fun systemLanguageTag(): String = browserLanguageTag()
