# Lumbre Hotel & Spa

Página de un hotel (ficticio) hecha con HTML, CSS y JavaScript sin dependencias ni proceso de build.

## Qué incluye

- **Fotografía real** en hero, habitaciones, experiencias y destino (17 fotos optimizadas en `assets/img`).
- **Animaciones**: titular palabra a palabra, parallax y zoom en el hero, escena "mañana → atardecer → noche" guiada por el scroll, apariciones con desenfoque, tarjetas con inclinación 3D y zoom de foto, contadores, mascota (Lumi) que reacciona al formulario y confeti al terminar. Respeta `prefers-reduced-motion`.
- **Todo es accionable**: las tarjetas de experiencias añaden extras al presupuesto, las de destino preparan una consulta y "Elegir" preselecciona la habitación.
- **Presupuesto en 3 pasos** con desglose en vivo: noches, suplemento de fin de semana (+15 %), extras, descuento por 7+ noches (−10 %), código promocional (`LUMBRE10`) e impuestos.
- **Validaciones**: correo (formato + sugerencia de erratas como `gmial.com`), fechas (no pasadas, salida posterior a la llegada, máx. 30 noches y 18 meses vista), teléfono, nombre, aforo por habitación y consentimiento.
- **Idiomas y moneda**: español, inglés, portugués y francés; EUR, USD, MXN, GBP, BRL y COP. Se eligen solos según el idioma del navegador y la región (zona horaria), y se pueden cambiar desde la cabecera.
- **Cookies con consentimiento**: `lumbre_consent` (necesaria) y `lumbre_prefs` (idioma, moneda y región; solo si se acepta).
- **Responsiva** de móvil a escritorio.

## Seguridad

- Content-Security-Policy estricta (`default-src 'self'`, sin scripts ni estilos en línea, sin recursos externos).
- Ningún rastreador ni llamada a terceros; la región se estima en el propio navegador, sin enviar la IP a nadie.
- Todo el texto dinámico se escribe con `textContent` (sin `innerHTML`); el contenido de las cookies se valida contra listas blancas.
- Anti-bots: campo trampa (honeypot), tiempo mínimo antes de enviar y pausa entre envíos.
- Cookies con `SameSite=Lax` y `Secure` bajo HTTPS. Los datos personales no se guardan en el navegador.

> La validación en el navegador mejora la experiencia, pero no sustituye a la del servidor. Los formularios todavía **no envían** nada: en `js/app.js` están marcados los dos puntos ("Aquí iría el envío real") donde conectar tu backend, que debe volver a validar todo. En producción conviene además enviar la CSP y `X-Frame-Options`/`frame-ancestors` como cabeceras HTTP.

## Verla en local

```bash
python -m http.server 4173
```

Y abre <http://localhost:4173>.

## Estructura

```
index.html        Contenido y formularios
assets/img/       Fotografías
css/styles.css    Tokens de diseño, componentes, animaciones y responsive
js/i18n.js        Traducciones
js/app.js         Validaciones, presupuesto, cookies, idioma/región y animaciones
```

Los tipos de cambio y precios son orientativos y están en `js/app.js` (`RATES`, `ROOMS`, `EXTRAS`).

## Créditos

Fotografías de [Unsplash](https://unsplash.com), usadas bajo la [licencia Unsplash](https://unsplash.com/license). La paleta (crema, arena, verde mar y dorado) y los tokens de espaciado, radios y tipografía están al inicio de `css/styles.css`.
