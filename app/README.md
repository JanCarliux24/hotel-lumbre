# Lumbre · App multiplataforma (Android, iOS y web)

Una sola base de código en **Kotlin Multiplatform + Compose Multiplatform**: la lógica y la interfaz están en `shared/`, y cada plataforma solo aporta un punto de entrada mínimo. Cualquier cambio en `shared/` se aplica a la vez en Android, iOS y web.

```
app/
├─ shared/       Código común: datos, precios, validaciones, idiomas, tema y pantallas
│  └─ src/
│     ├─ commonMain/   ← casi todo vive aquí
│     ├─ androidMain/  idioma del sistema (Android)
│     ├─ iosMain/      idioma del sistema + MainViewController (iOS)
│     └─ wasmJsMain/   idioma y región del navegador (web)
├─ androidApp/   Actividad Android (se abre en Android Studio)
├─ iosApp/       Proyecto Xcode que incrusta el framework "Shared"
└─ webApp/       Página HTML que carga la app compilada a Kotlin/Wasm
```

## Qué hace

- **Inicio**: portada con parallax, búsqueda rápida, carrusel de habitaciones, experiencias, destino y opiniones.
- **Habitaciones** y **detalle**, con transición de imagen compartida entre pantallas.
- **Reserva en 3 pasos**: fechas (selector con límites), huéspedes, habitación con control de aforo, extras, código promocional (`LUMBRE10`) y datos validados (correo con sugerencia de erratas, teléfono, nombre y consentimiento). El desglose se recalcula en vivo, con las mismas reglas de precio que la web estática.
- **Mis reservas**, cancelación y **llave digital**.
- **Perfil**: idioma (ES, EN, PT, FR) y moneda (EUR, USD, MXN, GBP, BRL, COP), detectados según el idioma y la región del dispositivo o navegador.
- **Panel administrativo**: indicadores, gráfica de ingresos, gestión de reservas, precios, disponibilidad y promociones. Sus cambios se reflejan al instante en el resto de la app.
- **Animaciones**: botones con canto que se hunde y rebote elástico, mascota Lumi que reacciona al formulario, confeti, contadores animados, apariciones escalonadas y vibración háptica en móvil.
- **Ambiente vacacional**: olas animadas al pie de las fotos, tarjetas translúcidas tipo cristal, iconos de playa que flotan (sombrilla, sol, velero) y una cinta continua con los momentos del viaje.
- **Tema claro por defecto** (blanco, turquesa, sol, coral y arena), con selector Claro, Oscuro o Sistema en el perfil y botón rápido de sol/luna en la portada.
- **Diseño adaptable**: barra inferior en móvil y raíl lateral en pantallas anchas.

## Normas por plataforma

Están centralizadas en `shared/.../platform/Platform.kt` (`Capabilities`):

| Función | Android / iOS | Web |
|---|---|---|
| Reservar y gestionar estancias | ✅ | ✅ |
| Llave digital (NFC, vibración) | ✅ | ❌ se indica "en la app móvil" |
| Panel administrativo | ❌ bloqueado, con explicación | ✅ |

El repositorio también impide las acciones administrativas si no se está en la web con sesión de administrador, aunque alguien llegue a esa pantalla.

## Cómo ejecutarla

**Android (Android Studio):** *File → Open* y elige la carpeta `app`. Espera a que sincronice Gradle, elige la configuración `androidApp` y pulsa *Run*.

Desde la terminal:

```bash
./gradlew :androidApp:installDebug
```

**Web:**

```bash
./gradlew :webApp:wasmJsBrowserDevelopmentRun
```

La versión optimizada se genera con `./gradlew :webApp:wasmJsBrowserDistribution` y queda en `webApp/build/dist/wasmJs/productionExecutable/`.

**iOS:** necesita un Mac con Xcode. Abre `iosApp/iosApp.xcodeproj` y ejecuta. El script de Xcode compila el framework con `./gradlew :shared:embedAndSignAppleFrameworkForXcode`. En Windows los destinos iOS se omiten al compilar.

## Datos y siguiente paso

Ahora los datos se guardan en cada dispositivo (SharedPreferences, NSUserDefaults o localStorage) mediante `HotelRepository`. Para que una reserva hecha en el móvil aparezca en el panel web hace falta un backend compartido (Supabase, Firebase o una API propia): basta con sustituir el almacenamiento del repositorio, sin tocar las pantallas. El modo administrador es una demostración sin contraseña; en producción debe ir detrás de un inicio de sesión con roles validado en el servidor.

## Tecnologías

Kotlin 2.4 · Compose Multiplatform 1.11 · Material 3 · Navigation Compose (rutas tipadas) · kotlinx-datetime · kotlinx-serialization · multiplatform-settings · AGP 9 · Gradle 9.4.

Fuentes Inter y Playfair Display (SIL Open Font License). Fotografías de Unsplash.
