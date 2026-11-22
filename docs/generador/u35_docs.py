"""Documentos de las Unidades 3 y 5 — Programación móvil y concurrente (TAP).

Cuatro documentos, uno por tema solicitado: interfaz gráfica, componentes síncronos/asíncronos,
acceso a datos y propuesta de la aplicación móvil (con su guía de uso).
"""
import os
from docgen import Doc, APPWEB, APK, REPO, ROOT

U = 'Unidades 3 y 5 · Programación móvil y concurrente'
QR = os.path.join(ROOT, 'docs', 'capturas', 'qr_descargas.png')


# ======================================================================================
# 1 — INTERFAZ GRÁFICA DE USUARIO
# ======================================================================================
def interfaz():
    d = Doc('U3_5/U35_1_Interfaz_Grafica_de_Usuario.docx', U, 'Documento 1',
            'Interfaz gráfica de usuario', 'Cómo está construida la interfaz móvil de Lumbre y cómo responde a lo que hace el usuario')
    d.toc(['Resumen', 'Pantallas de la aplicación móvil', 'Estructura de navegación', 'Sistema de diseño',
           'Componentes gráficos', 'Respuesta a las acciones del usuario', 'Consistencia entre pantallas',
           'Accesibilidad y adaptación', 'Diferencias móvil y web', 'Conclusión'])

    d.h1('1. Resumen')
    d.p('La interfaz de Lumbre Hotel & Spa está escrita una sola vez con Compose Multiplatform (Kotlin) y se ejecuta '
        'como app Android, app iOS y app web. Está pensada primero para el celular: una barra de navegación inferior, '
        'botones grandes, formularios cortos por pasos y mensajes claros en el idioma y la moneda del huésped.')
    d.table(['Aspecto', 'Decisión de diseño'], [
        ['Tecnología de UI', 'Compose Multiplatform 1.11 + Material 3 (componentes declarativos, un solo código)'],
        ['Navegación', 'Navigation Compose con rutas tipadas y barra inferior de pestañas'],
        ['Idiomas', 'Español, inglés, portugués y francés; cambian al instante sin reiniciar'],
        ['Monedas', 'EUR, USD, MXN, GBP, BRL y COP; todos los precios se recalculan en vivo'],
        ['Temas', 'Claro, oscuro o el del sistema'],
        ['Tipografía', 'Playfair Display (títulos) e Inter (texto), incluidas como recursos de la app'],
        ['Asistente', '"Lumi", un personaje que da pistas contextuales durante la reserva'],
    ], [4, 12], 'Decisiones principales de la interfaz')

    d.h1('2. Pantallas de la aplicación móvil')
    d.table(['Pantalla', 'Para qué sirve', 'Quién la ve'], [
        ['Inicio', 'Presentación del hotel, accesos rápidos a reservar y a ofertas', 'Todos'],
        ['Habitaciones', 'Catálogo con precio por noche, capacidad y detalle de cada habitación', 'Todos'],
        ['Detalle de habitación', 'Fotos, servicios incluidos y botón "Reservar"', 'Todos'],
        ['Reserva (3 pasos)', 'Fechas y huéspedes → extras y código promocional → datos y confirmación', 'Todos'],
        ['Ofertas', 'Códigos promocionales activos y paquetes', 'Todos'],
        ['Mis viajes', 'Reservas propias con estado y opción de cancelar', 'Huésped'],
        ['Perfil', 'Cuenta, idioma, moneda, tema y permisos del dispositivo', 'Todos'],
        ['Privacidad', 'Cookies, ubicación y borrado de datos', 'Todos'],
        ['Recepción', 'Llegadas del día y cambio de estado de reservas', 'Personal (STAFF)'],
        ['Administración', 'Precios, disponibilidad y promociones', 'ADMIN'],
        ['Superusuario', 'Roles, bloqueo de cuentas, parámetros y bitácora', 'SUPERADMIN'],
    ], [3.6, 9, 3.4], 'Inventario de pantallas')
    d.shots([('movil_01_inicio.jpg', 'Inicio'), ('movil_detalle_habitacion.jpg', 'Detalle'),
             ('movil_ofertas.jpg', 'Ofertas')], 4.6, 'Pantallas principales en Android')
    d.shots([('movil_reserva_paso1.jpg', 'Paso 1'), ('movil_reserva_paso2.jpg', 'Paso 2'),
             ('movil_reserva_paso3.jpg', 'Paso 3')], 4.6, 'Flujo de reserva en tres pasos')

    d.h1('3. Estructura de navegación')
    d.p('La barra inferior muestra solo las pestañas que corresponden al rol de la persona: un huésped ve Inicio, '
        'Habitaciones, Ofertas, Mis viajes, Perfil y Privacidad; el personal además ve Recepción, y así sucesivamente. '
        'Las pantallas secundarias (detalle, reserva, confirmación) se apilan sobre la pestaña y se cierran con la flecha '
        '"atrás" o con el gesto del sistema.')
    d.diagram('10_navegacion.png', 'Mapa de navegación de la app')
    d.diagram('15_user_flow.png', 'Flujo del usuario al reservar', 15)

    d.h1('4. Sistema de diseño')
    d.table(['Elemento', 'Valor', 'Uso'], [
        ['Color principal', 'Turquesa #0A7C86', 'Botones principales, enlaces, elementos activos'],
        ['Color de texto', 'Azul noche #16313A', 'Títulos y texto principal'],
        ['Acento', 'Ámbar #F4A63A', 'Ofertas, avisos, detalles festivos'],
        ['Error / éxito', 'Rojo y verde Material', 'Mensajes de validación y confirmación'],
        ['Radio de esquinas', '16–24 dp', 'Tarjetas, botones y diálogos'],
        ['Espaciado base', 'Múltiplos de 4 dp (8, 12, 16, 24)', 'Márgenes y separación entre elementos'],
        ['Área táctil mínima', '48 dp', 'Todos los botones y controles'],
    ], [3.6, 4.6, 7.8], 'Valores del sistema de diseño')

    d.h1('5. Componentes gráficos')
    d.table(['Componente', 'Dónde aparece', 'Comportamiento'], [
        ['LumbreButton (primario, secundario, texto)', 'Todas las pantallas', 'Se desactiva mientras hay datos inválidos o una operación en curso'],
        ['Campos de texto con validación', 'Reserva, cuenta, administración', 'Muestran el error debajo del campo al momento de escribir'],
        ['Selector de fechas', 'Reserva paso 1', 'Bloquea fechas pasadas y más allá del límite configurado'],
        ['Contadores (+ / −)', 'Adultos y niños', 'No permiten salir del rango permitido'],
        ['Chips seleccionables', 'Extras, idioma, moneda', 'Animación de rebote al seleccionar'],
        ['Tarjetas de habitación', 'Catálogo', 'Imagen, precio en la moneda elegida y estado de disponibilidad'],
        ['Diálogos de confirmación', 'Cancelar reserva, borrar cuenta', 'Piden confirmar acciones que no se pueden deshacer'],
        ['Snackbars', 'Toda la app', 'Avisos breves de éxito o error de red'],
        ['Indicador de progreso', 'Inicio de sesión, sincronización', 'Aparece mientras se espera la respuesta del servidor'],
        ['Confeti y Lumi', 'Confirmación de reserva', 'Retroalimentación positiva al terminar'],
    ], [4.8, 4.2, 7], 'Componentes de la interfaz')

    d.h1('6. Respuesta a las acciones del usuario')
    d.p('Cada acción tiene una respuesta visible en menos de un segundo, aunque la operación real con el servidor '
        'tarde más. Esto se logra separando la interfaz del trabajo en red (ver documento 2).')
    d.table(['Acción del usuario', 'Respuesta inmediata', 'Respuesta final'], [
        ['Cambia fechas o huéspedes', 'El presupuesto se recalcula al instante', '—'],
        ['Escribe un correo mal formado', 'Mensaje de error y sugerencia ("¿quisiste decir gmail.com?")', '—'],
        ['Aplica un código promocional', 'El descuento aparece en el total', 'Aviso si el código no existe o está inactivo'],
        ['Confirma la reserva', 'Pantalla de confirmación con referencia LMB-XXXXXX y confeti', 'La reserva se guarda en la nube en segundo plano'],
        ['Inicia sesión', 'El botón se desactiva y aparece un indicador de progreso', 'Entra a su cuenta o ve el motivo del error'],
        ['Cancela una reserva', 'Diálogo de confirmación', 'El estado cambia a "Cancelada" en la lista'],
        ['Cambia idioma o moneda', 'Toda la app cambia al momento', 'La preferencia se guarda en su perfil'],
        ['Pierde la conexión', 'La app sigue funcionando con los datos guardados', 'Aviso "sin conexión" al intentar guardar'],
    ], [4.2, 6, 5.8], 'Acciones y respuestas')
    d.shots([('movil_cancelar_dialogo.jpg', 'Confirmar cancelación'), ('movil_confirmacion.jpg', 'Reserva confirmada'),
             ('movil_mis_reservas.jpg', 'Mis viajes')], 4.6, 'Retroalimentación del sistema')

    d.h1('7. Consistencia entre pantallas')
    d.bullets([
        'Mismos colores, tipografías y radios en todas las pantallas, definidos en un solo tema (Theme.kt).',
        'La acción principal siempre está abajo a la derecha o a lo ancho, en turquesa; la secundaria, con contorno.',
        'Los errores siempre aparecen debajo del campo, en rojo y con texto que explica cómo corregirlo.',
        'Los precios siempre se muestran con el mismo formato de moneda y separador de miles del idioma elegido.',
        'Todos los textos salen del mismo catálogo de traducciones, así no hay pantallas a medio traducir.',
    ])

    d.h1('8. Accesibilidad y adaptación')
    d.bullets([
        'Contraste suficiente en tema claro y oscuro.',
        'Iconos con descripción para lectores de pantalla.',
        'Áreas táctiles de al menos 48 dp.',
        'El diseño se adapta del ancho de un teléfono al de una tableta o navegador sin cambiar de código.',
        'Respeta el tamaño de letra configurado en el sistema.',
    ])
    d.shots([('movil_02_preferencias_capacidades.jpg', 'Preferencias'), ('movil_cookies.jpg', 'Privacidad'),
             ('movil_aviso_region.jpg', 'Aviso de región')], 4.6, 'Preferencias y privacidad en el móvil')

    d.h1('9. Diferencias móvil y web')
    d.table(['Característica', 'App móvil', 'App web'], [
        ['Navegación', 'Barra inferior', 'Barra lateral en pantallas anchas'],
        ['Ubicación', 'GPS del dispositivo (con permiso)', 'Geolocalización del navegador (con permiso)'],
        ['Sin conexión', 'Funciona con los datos guardados', 'Depende de la caché del navegador'],
        ['Instalación', 'APK / tienda de apps', 'Solo abrir el enlace'],
        ['Paneles de personal', 'Disponibles, pensados para consultas rápidas', 'Más cómodos para capturas largas'],
    ], [4, 6, 6], 'Qué cambia entre plataformas')

    d.h1('10. Conclusión')
    d.p('La interfaz móvil se organizó alrededor de la tarea principal —reservar— con pasos cortos, validación en '
        'el momento y una respuesta visible a cada acción. Al compartir un solo código de interfaz, el comportamiento '
        'es igual en Android, iOS y web, y los cambios de diseño se aplican en todas las plataformas a la vez.')
    return d.save()


# ======================================================================================
# 2 — COMPONENTES Y LIBRERÍAS SÍNCRONOS Y ASÍNCRONOS
# ======================================================================================
def concurrencia():
    d = Doc('U3_5/U35_2_Componentes_Sincronos_y_Asincronos.docx', U, 'Documento 2',
            'Componentes y librerías síncronos y asíncronos', 'Coroutines, flujos de estado y peticiones de red sin bloquear la interfaz')
    d.toc(['Conceptos', 'Librerías utilizadas', 'Qué es síncrono y qué es asíncrono en la app', 'Modelo de concurrencia',
           'Flujos de estado (StateFlow y SharedFlow)', 'Ejemplo: guardar una reserva', 'Ejemplo: iniciar sesión',
           'Manejo de errores y cancelación', 'Pruebas', 'Conclusión'])

    d.h1('1. Conceptos')
    d.table(['Concepto', 'Significado en la app'], [
        ['Síncrono', 'La instrucción termina antes de pasar a la siguiente. Se usa para cálculos rápidos en memoria '
         '(presupuesto, validaciones, formato de moneda).'],
        ['Asíncrono', 'La operación se lanza y la app sigue respondiendo; el resultado llega después. Se usa para todo '
         'lo que viaja por la red (Firebase) o tarda.'],
        ['Hilo principal (UI)', 'Dibuja la pantalla y atiende toques. Nunca se usa para esperar a la red.'],
        ['Coroutine', 'Tarea ligera de Kotlin que puede suspenderse sin bloquear el hilo donde corre.'],
        ['suspend fun', 'Función que puede pausarse mientras espera (por ejemplo, una respuesta HTTP).'],
        ['Dispatcher', 'Decide en qué hilos corre una coroutine: Main para la UI, Default para trabajo en segundo plano.'],
    ], [3.6, 12.4], 'Conceptos de concurrencia')

    d.h1('2. Librerías utilizadas')
    d.table(['Librería', 'Versión', 'Tipo', 'Uso en Lumbre'], [
        ['kotlinx.coroutines', '1.11', 'Asíncrona', 'Coroutines, scopes, dispatchers, StateFlow y SharedFlow'],
        ['Ktor Client', '3.5.1', 'Asíncrona', 'Peticiones HTTP a Firebase Auth y Firestore (REST)'],
        ['kotlinx.serialization', '1.9', 'Síncrona', 'Convertir JSON ↔ objetos Kotlin'],
        ['kotlinx.datetime', '0.7', 'Síncrona', 'Fechas de entrada/salida, noches y límites'],
        ['multiplatform-settings', '1.3', 'Síncrona', 'Guardar preferencias y caché local en el dispositivo'],
        ['Compose Multiplatform', '1.11.1', 'Reactiva', 'Interfaz que se redibuja cuando cambia el estado'],
        ['Navigation Compose', '2.9.2', 'Síncrona', 'Cambio de pantallas'],
    ], [4, 1.8, 2.2, 8], 'Librerías síncronas y asíncronas')
    d.diagram('09_dependencias_externas.png', 'Dependencias externas de la app', 15)

    d.h1('3. Qué es síncrono y qué es asíncrono en la app')
    d.table(['Operación', 'Modo', 'Por qué'], [
        ['Calcular el presupuesto (Pricing.quote)', 'Síncrono', 'Es aritmética en memoria; tarda microsegundos'],
        ['Validar nombre, correo, teléfono, fechas (Validation)', 'Síncrono', 'Se ejecuta en cada tecla y debe responder al instante'],
        ['Guardar preferencias locales', 'Síncrono', 'Escritura pequeña en el almacenamiento del dispositivo'],
        ['Registrar / iniciar sesión', 'Asíncrono', 'Viaja a Firebase Authentication'],
        ['Descargar habitaciones, promociones y parámetros', 'Asíncrono', 'Lectura de Firestore al abrir la app'],
        ['Guardar o cancelar una reserva', 'Asíncrono', 'Escritura en Firestore en segundo plano'],
        ['Renovar el token de sesión', 'Asíncrono', 'Petición a Secure Token antes de que caduque'],
        ['Registrar en la bitácora', 'Asíncrono', 'Escritura adicional que no debe retrasar al usuario'],
        ['Obtener la ubicación', 'Asíncrono', 'Depende del GPS o del navegador'],
    ], [6.4, 2.4, 7.2], 'Clasificación de operaciones')

    d.h1('4. Modelo de concurrencia')
    d.p('El repositorio (HotelRepository) tiene su propio ámbito de coroutines con un SupervisorJob y el dispatcher '
        'Default. Así, el trabajo de red corre fuera del hilo de la interfaz y, si una tarea falla, las demás siguen vivas.')
    d.code('private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)\n\n'
           '/** Ejecuta una escritura en la nube en segundo plano; si falla, avisa y vuelve a sincronizar. */\n'
           'private fun remote(block: suspend () -> Unit) {\n'
           '    if (!cloud || _account.value == null) return\n'
           '    scope.launch {\n'
           '        try { block() } catch (e: Throwable) { _events.tryEmit(mapError(e)); refreshAll() }\n'
           '    }\n'
           '}', 'HotelRepository.kt — ámbito y escrituras en segundo plano')
    d.diagram('14_concurrencia.png', 'Hilos, coroutines y flujos de estado')
    d.table(['Pieza', 'Cantidad / ubicación'], [
        ['Funciones suspend', '34 (repositorio y clientes de Firebase)'],
        ['Ámbito del repositorio', '1 CoroutineScope con SupervisorJob + Dispatchers.Default'],
        ['Ámbitos de pantalla', 'rememberCoroutineScope en formularios de cuenta; LaunchedEffect para cargas y animaciones'],
        ['Estados observables', 'Más de 10 StateFlow (preferencias, habitaciones, promociones, reservas, parámetros, cuenta, usuarios, bitácora, sincronización, rol…)'],
        ['Eventos', '1 SharedFlow para avisos de error o éxito'],
        ['Estado derivado', 'combine(cuenta, preferencias) calcula el rol vigente'],
    ], [4.4, 11.6], 'Inventario de concurrencia')

    d.h1('5. Flujos de estado (StateFlow y SharedFlow)')
    d.p('La interfaz no pregunta por los datos: se suscribe a ellos. Cuando una coroutine actualiza un StateFlow, '
        'Compose redibuja solo las partes que dependen de ese valor.')
    d.code('private val _reservations = MutableStateFlow(load(KEY_RES) { ... })\n'
           'val reservations: StateFlow<List<Reservation>> = _reservations.asStateFlow()\n\n'
           '// En la pantalla\n'
           'val rooms by repo.rooms.collectAsState()\n'
           'val params by repo.params.collectAsState()', 'Publicar y observar estado')
    d.pros_cons(['La UI siempre muestra el último valor', 'Sin bloqueos ni callbacks anidados',
                 'Mismo código en Android, iOS y web'],
                ['Hay que exponer solo versiones de lectura', 'Requiere entender el ciclo de vida de las coroutines'],
                'Ventajas y desventajas del modelo reactivo')

    d.h1('6. Ejemplo: guardar una reserva')
    d.p('Al confirmar, la reserva se agrega primero a la lista local (respuesta inmediata) y después se envía a '
        'Firestore en segundo plano. Si la escritura falla, el usuario recibe un aviso y la app vuelve a sincronizar.')
    d.code('fun book(draft: Reservation): Reservation? {\n'
           '    lastBooking?.let { if (it.elapsedNow().inWholeSeconds < _params.value.bookingCooldownSec) return null }\n'
           '    lastBooking = TimeSource.Monotonic.markNow()\n'
           '    val saved = draft.copy(ref = newRef(), status = ReservationStatus.CONFIRMED, ...)\n'
           '    _reservations.update { listOf(saved) + it }          // síncrono: la UI cambia ya\n'
           '    save(KEY_RES, _reservations.value)                    // síncrono: caché local\n'
           '    if (acc != null) remote { fs.set("reservations/${saved.ref}", ...) } // asíncrono\n'
           '    return saved\n'
           '}', 'Reserva: parte síncrona y parte asíncrona')
    d.diagram('06_secuencia_reserva.png', 'Secuencia al crear una reserva', 15)

    d.h1('7. Ejemplo: iniciar sesión')
    d.p('El formulario lanza la operación con rememberCoroutineScope. Mientras espera, el botón queda deshabilitado '
        'y aparece un indicador de progreso; el resto de la app sigue respondiendo.')
    d.code('LumbreButton(t(K.ACC_SIGNIN), enabled = !busy, onClick = {\n'
           '    scope.launch {\n'
           '        busy = true\n'
           '        error = repo.login(email, password)   // suspend: no bloquea\n'
           '        busy = false\n'
           '    }\n'
           '})\n'
           'if (busy) CircularProgressIndicator()', 'AccountSection.kt — inicio de sesión')
    d.diagram('07_secuencia_login.png', 'Secuencia de inicio de sesión', 15)

    d.h1('8. Manejo de errores y cancelación')
    d.bullets([
        'SupervisorJob: el fallo de una escritura no cancela las demás tareas del repositorio.',
        'guarded { }: envuelve las operaciones de cuenta y devuelve un mensaje traducido en lugar de lanzar la excepción a la UI.',
        'mapError: traduce los códigos de Firebase (EMAIL_EXISTS, INVALID_PASSWORD, PERMISSION_DENIED…) a mensajes claros.',
        'Las coroutines de pantalla se cancelan solas al salir de ella (rememberCoroutineScope / LaunchedEffect).',
        'El token se renueva antes de caducar (60 s de margen), así no se interrumpe una operación por sesión vencida.',
        'Tiempo de espera entre reservas (bookingCooldownSec) para evitar reservas duplicadas por doble toque.',
    ])

    d.h1('9. Pruebas')
    d.p('La lógica síncrona (presupuestos y validaciones) tiene 14 pruebas unitarias que se ejecutan con:')
    d.code('./gradlew :shared:testAndroidHostTest', 'Ejecutar las pruebas')
    d.table(['Archivo', 'Qué comprueba'], [
        ['PricingTest.kt', 'Noches, impuestos, extras, descuentos y estancias largas'],
        ['ValidationTest.kt', 'Nombre, correo y su sugerencia, teléfono, fechas, contraseña y códigos promocionales'],
    ], [4, 12], 'Pruebas unitarias')

    d.h1('10. Conclusión')
    d.p('La app separa lo que debe ser instantáneo (cálculos y validaciones, síncronos) de lo que depende de la red '
        '(Firebase, asíncrono con coroutines). La interfaz observa flujos de estado, por lo que nunca espera a la red '
        'y siempre muestra el dato más reciente.')
    return d.save()


# ======================================================================================
# 3 — ACCESO A DATOS
# ======================================================================================
def datos():
    d = Doc('U3_5/U35_3_Acceso_a_Datos.docx', U, 'Documento 3',
            'Acceso a datos', 'Consultar, guardar y actualizar información de forma correcta, segura y coherente')
    d.toc(['Arquitectura de datos', 'Dónde vive cada dato', 'Consultas', 'Altas', 'Actualizaciones y bajas',
           'Seguridad', 'Coherencia de los datos', 'Funcionamiento sin conexión', 'Conclusión'])

    d.h1('1. Arquitectura de datos')
    d.p('La app usa Firebase (plan gratuito Spark): Authentication para las cuentas y Cloud Firestore como base de '
        'datos documental. Se accede por su API REST con Ktor, lo que permite usar el mismo código en Android, iOS y web. '
        'Toda la app pasa por un único punto de acceso: HotelRepository.')
    d.diagram('04_arquitectura.png', 'Capas de la aplicación', 15)
    d.table(['Capa', 'Archivo', 'Responsabilidad'], [
        ['Interfaz', 'ui/screens/*.kt', 'Muestra datos y recoge acciones; nunca llama a la red directamente'],
        ['Repositorio', 'data/HotelRepository.kt', 'Fuente única de verdad: caché, permisos, sincronización'],
        ['Mapeo', 'data/firebase/Mappers.kt', 'Convierte documentos de Firestore ↔ modelos Kotlin'],
        ['Clientes REST', 'data/firebase/FirebaseApi.kt', 'Peticiones a Auth y Firestore con el token del usuario'],
        ['Reglas', 'firebase/firestore.rules', 'Validan permisos y datos en el servidor'],
    ], [2.8, 5, 8.2], 'Capas de acceso a datos')

    d.h1('2. Dónde vive cada dato')
    d.diagram('11_modelo_nosql_firestore.png', 'Colecciones de Firestore', 15)
    d.table(['Colección', 'Contenido', 'Lectura', 'Escritura'], [
        ['users/{uid}', 'Nombre, correo, teléfono, rol, preferencias', 'El propio usuario y el personal', 'El usuario (sus datos) · superusuario (rol y bloqueo)'],
        ['rooms/{id}', 'Precio por noche, capacidad, disponibilidad', 'Pública', 'Administración'],
        ['promos/{code}', 'Porcentaje de descuento y si está activo', 'Pública', 'Administración'],
        ['config/params', 'Impuesto, noches máximas, longitud de contraseña…', 'Pública', 'Superusuario'],
        ['reservations/{ref}', 'Habitación, fechas, huéspedes, total, estado', 'El dueño y el personal', 'El dueño crea y cancela · personal cambia estado'],
        ['audit/{id}', 'Quién hizo qué y cuándo', 'Superusuario', 'Personal (solo alta, nunca se edita)'],
    ], [3, 4.6, 3.6, 4.8], 'Colecciones y permisos')

    d.h1('3. Consultas')
    d.table(['Consulta', 'Método', 'Cuándo se hace'], [
        ['Habitaciones, promociones y parámetros', 'fs.list("rooms"), fs.list("promos"), fs.get("config/params")', 'Al abrir la app'],
        ['Mis reservas (huésped)', 'fs.whereEquals("reservations", "uid", uid)', 'Al iniciar sesión y al refrescar'],
        ['Todas las reservas (personal)', 'fs.list("reservations")', 'Al abrir Recepción'],
        ['Usuarios y bitácora', 'fs.list("users"), fs.list("audit")', 'Solo para el superusuario'],
    ], [4.6, 7, 4.4], 'Consultas principales')
    d.code('val docs = if (acc.role.atLeast(Role.STAFF)) fs.list("reservations")\n'
           '           else fs.whereEquals("reservations", "uid", acc.uid)', 'Cada rol consulta solo lo que puede ver')

    d.h1('4. Altas')
    d.bullets([
        'Registro: Firebase Auth crea la cuenta y la app crea users/{uid} siempre con rol GUEST.',
        'Reserva: se crea reservations/LMB-XXXXXX con estado CONFIRMED y el uid del dueño.',
        'Promoción: administración crea promos/{CÓDIGO}.',
        'Bitácora: cada cambio administrativo agrega un registro en audit.',
    ])

    d.h1('5. Actualizaciones y bajas')
    d.table(['Operación', 'Quién', 'Campos que puede cambiar'], [
        ['Editar perfil', 'El usuario', 'name, phone, lang, currency, theme'],
        ['Cancelar reserva', 'El dueño', 'status → CANCELLED'],
        ['Cambiar estado de reserva', 'Personal', 'status → CONFIRMED / CHECKED_IN / CANCELLED'],
        ['Precio o disponibilidad', 'Administración', 'nightlyEur (30–5000), available'],
        ['Rol o bloqueo de cuenta', 'Superusuario', 'role, disabled (nunca sobre sí mismo)'],
        ['Borrar cuenta', 'El usuario o el superusuario', 'Elimina users/{uid} y la cuenta de Auth'],
    ], [4, 3.6, 8.4], 'Actualizaciones permitidas')

    d.h1('6. Seguridad')
    d.diagram('13_reglas_firebase.png', 'Reglas de seguridad de Firestore', 15)
    d.table(['Medida', 'Cómo funciona'], [
        ['Autenticación', 'Correo y contraseña con Firebase Auth; token de 1 h renovado automáticamente'],
        ['Autorización en el servidor', 'Las reglas comprueban rol y dueño en cada lectura o escritura; la app no puede saltárselas'],
        ['Autorización en la app', 'require(Role) antes de cada operación administrativa y menús según el rol'],
        ['Validación doble', 'Validation.kt en la app y las mismas reglas de formato y rango en firestore.rules'],
        ['Mínimo privilegio', 'Cada usuario solo lee sus reservas; nadie puede asignarse un rol'],
        ['Cambios acotados', 'onlyChanges([...]) impide modificar campos no permitidos'],
        ['Bitácora inmutable', 'audit no admite update ni delete'],
        ['Cerrado por defecto', 'Cualquier ruta no declarada se rechaza'],
        ['Transporte', 'HTTPS en todas las peticiones'],
        ['Privacidad', 'Ubicación y cookies solo con consentimiento; el usuario puede borrar sus datos'],
    ], [4, 12], 'Medidas de seguridad')
    d.code('match /reservations/{ref} {\n'
           '  allow read: if signedIn() && (resource.data.uid == request.auth.uid || isStaff());\n'
           '  allow update: if (signedIn() && resource.data.uid == request.auth.uid\n'
           '      && onlyChanges([\'status\']) && request.resource.data.status == \'CANCELLED\')\n'
           '    || (isStaff() && onlyChanges([\'status\']) ...);\n'
           '}', 'firestore.rules — reservas')

    d.h1('7. Coherencia de los datos')
    d.bullets([
        'Una sola fuente de verdad (HotelRepository) para toda la interfaz.',
        'Las referencias de reserva siguen el formato LMB- más 6 caracteres y las reglas lo verifican.',
        'La fecha de salida siempre es posterior a la de entrada (app y servidor).',
        'Los totales se calculan con la misma función de presupuesto que ve el usuario.',
        'Si una escritura falla, la app vuelve a descargar los datos (refreshAll) para no quedar desincronizada.',
        'Las habitaciones que faltan en la nube se completan con los valores por defecto.',
    ])
    d.diagram('17_estados_reserva.png', 'Estados posibles de una reserva', 13)

    d.h1('8. Funcionamiento sin conexión')
    d.p('Preferencias, habitaciones, promociones, parámetros y reservas se guardan también en el dispositivo con '
        'multiplatform-settings. Al abrir la app sin red se muestran esos datos; al recuperar la conexión, '
        'refreshAll() vuelve a sincronizar.')
    d.pros_cons(['La app abre al instante', 'Se puede consultar una reserva sin red', 'Menos lecturas a Firestore (plan gratuito)'],
                ['Los datos pueden estar unos segundos desactualizados', 'Hay que resolver diferencias al sincronizar'],
                'Caché local')

    d.h1('9. Conclusión')
    d.p('El acceso a datos está centralizado en el repositorio, protegido en el servidor por reglas de Firestore y '
        'validado también en la app. Cada rol consulta y modifica solo lo que le corresponde, y la caché local mantiene '
        'la app usable aun sin conexión.')
    return d.save()


# ======================================================================================
# 4 — PROPUESTA DE APLICACIÓN MÓVIL + USO
# ======================================================================================
def propuesta():
    d = Doc('U3_5/U35_4_Propuesta_de_Aplicacion_Movil.docx', U, 'Documento 4',
            'Propuesta de aplicación móvil', 'Problema, usuarios, funciones, conceptos móviles y concurrentes, y guía de uso de la app')
    d.toc(['Problema', 'Usuarios', 'Funciones principales', 'Programación móvil aplicada', 'Programación concurrente aplicada',
           'Tecnologías', 'Uso de la aplicación móvil', 'Descarga e instalación', 'Conclusión'])

    d.h1('1. Problema')
    d.p('Lumbre es un hotel boutique que recibía reservas por teléfono, correo y hojas de cálculo. Eso provocaba '
        'respuestas lentas, precios que el huésped conocía hasta el final, errores al copiar datos y reservas duplicadas. '
        'Los huéspedes, en su mayoría, planean el viaje desde el celular.')
    d.table(['Situación actual', 'Con la aplicación'], [
        ['Varias llamadas o correos para reservar', 'Reserva completa en menos de un minuto'],
        ['Precio final desconocido hasta el final', 'Presupuesto en vivo con impuestos, extras y descuentos'],
        ['Datos capturados a mano', 'Datos validados al escribir y guardados directamente'],
        ['Sin consulta posterior', '"Mis viajes" con estado y opción de cancelar'],
        ['El personal revisa hojas de cálculo', 'Recepción, administración y superusuario en la misma app'],
    ], [8, 8], 'Problema y respuesta')

    d.h1('2. Usuarios')
    d.table(['Usuario', 'Rol', 'Qué necesita'], [
        ['Huésped', 'GUEST', 'Ver habitaciones, reservar, consultar y cancelar sus reservas'],
        ['Recepcionista', 'STAFF', 'Ver llegadas, registrar entradas y cancelar'],
        ['Administrador', 'ADMIN', 'Ajustar precios, disponibilidad y promociones'],
        ['Superusuario', 'SUPERADMIN', 'Gestionar cuentas y roles, parámetros y revisar la bitácora'],
    ], [3.4, 3, 9.6], 'Usuarios de la app')
    d.diagram('05_casos_uso.png', 'Casos de uso por rol', 15)

    d.h1('3. Funciones principales')
    d.bullets([
        'Catálogo de habitaciones con precio en la moneda del usuario.',
        'Reserva en tres pasos con presupuesto en vivo, extras y códigos promocionales.',
        'Confirmación con referencia única y consulta en "Mis viajes".',
        'Cancelación de reservas propias.',
        'Cuentas con correo y contraseña, verificación y recuperación de contraseña.',
        'Cuatro idiomas, seis monedas y tema claro/oscuro.',
        'Privacidad: cookies, ubicación con consentimiento y borrado de datos.',
        'Paneles de recepción, administración y superusuario con bitácora.',
    ])

    d.h1('4. Programación móvil aplicada')
    d.table(['Concepto', 'Aplicación en Lumbre'], [
        ['Multiplataforma', 'Kotlin Multiplatform: un código para Android, iOS y web; solo ubicación y plataforma tienen código específico (expect/actual)'],
        ['Interfaz declarativa', 'Compose: la pantalla se describe a partir del estado y se redibuja sola'],
        ['Ciclo de vida', 'Las tareas de pantalla se cancelan al salir; el estado sobrevive a la rotación'],
        ['Navegación', 'Pila de pantallas con rutas tipadas y botón "atrás" del sistema'],
        ['Permisos', 'Ubicación solicitada en tiempo de ejecución y solo tras aceptar'],
        ['Almacenamiento local', 'Preferencias y caché en el dispositivo'],
        ['Recursos', 'Fuentes, imágenes y textos traducidos empaquetados con la app'],
        ['Distribución', 'APK para Android y versión web publicada en GitHub Pages'],
    ], [4, 12], 'Conceptos de programación móvil')

    d.h1('5. Programación concurrente aplicada')
    d.table(['Concepto', 'Aplicación en Lumbre'], [
        ['Coroutines', '34 funciones suspend para red y autenticación'],
        ['Ámbito propio', 'CoroutineScope(SupervisorJob() + Dispatchers.Default) en el repositorio'],
        ['No bloquear la UI', 'La red corre en segundo plano; la UI solo observa el resultado'],
        ['Estado compartido', 'StateFlow para datos y SharedFlow para avisos'],
        ['Estado derivado', 'combine() calcula el rol a partir de cuenta y preferencias'],
        ['Tareas de pantalla', 'LaunchedEffect y rememberCoroutineScope'],
        ['Tolerancia a fallos', 'SupervisorJob, guarded y resincronización automática'],
        ['Concurrencia de usuarios', 'Reglas de Firestore y tiempo de espera entre reservas evitan conflictos y duplicados'],
    ], [4, 12], 'Conceptos de programación concurrente')

    d.h1('6. Tecnologías')
    d.table(['Área', 'Tecnología'], [
        ['Lenguaje', 'Kotlin 2.4'], ['Interfaz', 'Compose Multiplatform 1.11, Material 3'],
        ['Red', 'Ktor 3.5 (REST)'], ['Backend', 'Firebase Authentication + Cloud Firestore'],
        ['Concurrencia', 'kotlinx.coroutines'], ['Construcción', 'Gradle 9.4, Android Gradle Plugin 9.2'],
        ['Código fuente', REPO],
    ], [4, 12], 'Tecnologías del proyecto')

    d.h1('7. Uso de la aplicación móvil')
    d.p('Esta sección recorre la app en Android tal como la usa un huésped, de la primera apertura a la cancelación.')

    d.h2('7.1 Primera apertura')
    d.p('Al abrir la app aparece el aviso de cookies. El usuario elige qué acepta; si permite la ubicación, la app '
        'propone el idioma y la moneda de su país.')
    d.shots([('movil_cookies.jpg', '1. Aviso de cookies'), ('movil_aviso_region.jpg', '2. Idioma y moneda sugeridos'),
             ('movil_01_inicio.jpg', '3. Pantalla de inicio')], 4.6, 'Primera apertura')

    d.h2('7.2 Explorar habitaciones y ofertas')
    d.p('Desde la barra inferior se abren Habitaciones y Ofertas. Al tocar una habitación se ve su detalle con precio, '
        'capacidad y servicios.')
    d.shots([('movil_detalle_habitacion.jpg', '4. Detalle de habitación'), ('movil_ofertas.jpg', '5. Ofertas y códigos')],
            5.4, 'Explorar')

    d.h2('7.3 Reservar')
    d.bullets(['Paso 1: elegir fechas, adultos y niños. El total se actualiza al instante.',
               'Paso 2: añadir extras (desayuno, spa, traslado…) y, si se tiene, un código promocional.',
               'Paso 3: escribir nombre, correo y teléfono. Los errores se marcan al escribir.',
               'Confirmar: aparece la referencia LMB-XXXXXX y la reserva queda en "Mis viajes".'], numbered=True)
    d.shots([('movil_reserva_paso1.jpg', '6. Fechas y huéspedes'), ('movil_reserva_paso2.jpg', '7. Paso 2'),
             ('movil_reserva_extras.jpg', '8. Extras')], 4.6, 'Reserva, pasos 1 y 2')
    d.shots([('movil_reserva_paso3.jpg', '9. Datos del huésped'), ('movil_confirmacion.jpg', '10. Confirmación')],
            5.4, 'Reserva, paso 3 y confirmación')

    d.h2('7.4 Consultar y cancelar')
    d.p('En "Mis viajes" se ven todas las reservas con su estado. Para cancelar, se toca la reserva y se confirma en '
        'el diálogo; el estado cambia a "Cancelada".')
    d.shots([('movil_mis_reservas.jpg', '11. Mis viajes'), ('movil_cancelar_dialogo.jpg', '12. Confirmar cancelación')],
            5.4, 'Consultar y cancelar')

    d.h2('7.5 Preferencias y cuenta')
    d.p('En Perfil se cambia idioma, moneda y tema, se inicia sesión o se crea una cuenta, y se revisan los permisos '
        'del dispositivo (ubicación, notificaciones).')
    d.shot('movil_02_preferencias_capacidades.jpg', '13. Perfil: preferencias y capacidades del dispositivo', 6)

    d.h2('7.6 Personal del hotel')
    d.p('Con una cuenta de personal aparecen pestañas extra. Recepción muestra las llegadas del día; Administración '
        'permite cambiar precios y promociones; el superusuario gestiona roles, parámetros y la bitácora.')
    d.shots([('escritorio_recepcion.jpg', 'Recepción'), ('escritorio_admin_panel.jpg', 'Administración'),
             ('escritorio_super_seguridad.jpg', 'Superusuario')], 5.2, 'Paneles del personal')

    d.h1('8. Descarga e instalación')
    d.image(QR, 'Códigos QR de descarga', 15)
    d.table(['Plataforma', 'Enlace', 'Pasos'], [
        ['Android (APK)', APK, '1. Escanear el QR o abrir el enlace. 2. Descargar lumbre.apk. 3. Permitir "instalar apps '
         'desconocidas" para el navegador. 4. Abrir el archivo e instalar.'],
        ['Web', APPWEB, 'Escanear el QR o abrir el enlace en cualquier navegador moderno; no requiere instalación.'],
    ], [3, 6, 7], 'Enlaces de descarga')
    d.note('La APK es una versión de prueba (debug) firmada con la llave de desarrollo; Android mostrará un aviso '
           'antes de instalarla.', 'Nota')

    d.h1('9. Conclusión')
    d.p('Lumbre convierte un proceso de reserva lento y manual en una app móvil rápida y clara para huéspedes y '
        'personal. Aplica conceptos de programación móvil (multiplataforma, interfaz declarativa, permisos, ciclo de '
        'vida) y concurrente (coroutines, flujos de estado, trabajo en segundo plano) para que la interfaz responda '
        'siempre, incluso mientras se comunica con la nube.')
    return d.save()


ALL = [interfaz, concurrencia, datos, propuesta]

if __name__ == '__main__':
    for fn in ALL:
        print(fn())
