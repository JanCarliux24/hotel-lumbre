"""Entregables de la Unidad 1 — Diseño y desarrollo de una interfaz centrada en el usuario."""
import os
from docgen import Doc, WEB, APPWEB, APK, REPO, ROOT

U = 'Unidad 1 · Diseño y desarrollo de una interfaz centrada en el usuario'
VIDEO = 'Prado_JanCarlo_Unidad1.mp4'
ZIP = 'Prado_JanCarlo_Unidad1.zip'



# ======================================================================================
# E1 — DOCUMENTO PRINCIPAL
# ======================================================================================
def e1():
    d = Doc('U1/U1_E1_Documento_Interfaz_Centrada_en_el_Usuario.docx', U, 'Entregable 1 · Documento',
            'Interfaz centrada en el usuario', 'Lumbre Hotel & Spa: de la oportunidad a una interfaz fácil de usar en Android, iOS y web')
    d.toc(['Descripción de la oportunidad', 'Usuario objetivo', 'User Persona', 'Necesidades identificadas',
           'Principios UX utilizados', 'User Flow', 'Wireframes y prototipo', 'Descripción de la aplicación',
           'Capturas de las pantallas desarrolladas', 'Componentes gráficos utilizados', 'Navegación e interacción',
           'Validaciones implementadas', 'Retroalimentación del sistema', 'Evidencias de la prueba de usabilidad',
           'Problemas encontrados', 'Mejoras realizadas y propuestas', 'Reflexión y conclusiones'])

    # 1 -------------------------------------------------------------------------------
    d.h1('1. Descripción de la oportunidad')
    d.note('La actividad pide identificar una "problemática". En este proyecto la planteamos como una oportunidad: '
           'una situación que hoy funciona, pero mal, y que una buena interfaz puede convertir en una ventaja para el '
           'hotel y para sus huéspedes.', 'Enfoque')
    d.table(['Pregunta', 'Respuesta'], [
        ['¿Cuál es la oportunidad?', 'Convertir la reserva de un hotel boutique —hoy hecha por teléfono, correo y hojas de cálculo— '
         'en una experiencia de menos de un minuto, clara, sin errores y en el idioma y la moneda del huésped.'],
        ['¿Quién la tiene?', 'Huéspedes nacionales e internacionales que planean vacaciones desde el celular, y el personal '
         'de recepción y administración que hoy reescribe los datos a mano.'],
        ['¿En qué contexto ocurre?', 'Al planear un viaje: en casa o en el trabajo, muchas veces desde el móvil, comparando '
         'precios y fechas, con poca paciencia para formularios largos.'],
        ['¿Cómo se resuelve hoy?', 'Llamadas y correos de ida y vuelta; el precio final se conoce al final; hay errores de '
         'captura (correos mal escritos, fechas imposibles) y reservas duplicadas.'],
        ['¿Cómo ayuda una aplicación?', 'Presupuesto en vivo con impuestos y extras, validación en el momento, confirmación '
         'inmediata con referencia, consulta de "Mis reservas" desde cualquier dispositivo y paneles para el personal.'],
        ['¿Cómo la llevamos a cabo?', 'Seguimos el proceso del curso: usuario → necesidades → UX (user flow, principios) → '
         'UI (wireframes) → desarrollo en Kotlin Multiplatform → pruebas → mejoras, en ciclos cortos con revisiones.'],
    ], [4.2, 11.8], 'La oportunidad en seis preguntas')
    d.p('Proceso aplicado:', bold_prefix='')
    d.bullets(['Identificación de la oportunidad → identificación del usuario → análisis de necesidades → diseño de experiencia (UX) '
               '→ diseño de interfaz (UI) → desarrollo → pruebas con usuarios → identificación de mejoras.'])

    # 2 -------------------------------------------------------------------------------
    d.h1('2. Usuario objetivo')
    d.table(['Característica', 'Huésped (usuario principal)', 'Personal del hotel (usuario secundario)'], [
        ['Rango de edad', '25–55 años', '22–50 años'],
        ['Ocupación', 'Profesionistas, parejas y familias que vacacionan 1–3 veces al año', 'Recepcionistas, administración, dirección'],
        ['Contexto de uso', 'Celular en casa, transporte o trabajo; a veces computadora para comparar', 'Computadora de recepción y móvil del turno'],
        ['Experiencia tecnológica', 'Media: usa apps de banco, mensajería y compras', 'Media–alta'],
        ['Necesidades', 'Precio total claro, en su moneda; reservar rápido; ver y cancelar su reserva', 'Ver llegadas del día, cambiar estados, ajustar precios'],
        ['Limitaciones relevantes', 'Poca paciencia, pantalla pequeña, conexión variable, distintos idiomas', 'Interrupciones constantes, turnos de 24 h'],
    ], [3.3, 6.5, 6.2], 'Usuarios objetivo')

    # 3 -------------------------------------------------------------------------------
    d.h1('3. User Persona')
    d.table(['Elemento', 'Descripción'], [
        ['Nombre', 'Mariana López (persona ficticia)'],
        ['Edad', '34 años'],
        ['Ocupación', 'Arquitecta en Guadalajara; viaja 2–3 veces al año con su pareja'],
        ['Experiencia tecnológica', 'Media: compra en línea y usa banca móvil, pero no le gustan las apps complicadas'],
        ['Necesidades', 'Saber cuánto pagará en pesos, con impuestos, antes de dar sus datos; reservar desde el celular en sus descansos'],
        ['Objetivos', 'Reservar 3 noches frente al mar en menos de 5 minutos y poder consultar la reserva después'],
        ['Frustraciones', 'Formularios largos que se borran al equivocarse; mensajes como "Dato incorrecto"; precios en euros; costos ocultos al final'],
        ['Cita', '"Si no veo el precio final rápido, cierro la página."'],
    ], [4, 12], 'User Persona')

    # 4 -------------------------------------------------------------------------------
    d.h1('4. Necesidades identificadas')
    d.table(['#', 'Necesidad concreta', 'Respuesta en la interfaz'], [
        ['N1', 'El usuario necesita conocer el precio total (con impuestos y extras) en su moneda antes de capturar sus datos.', 'Presupuesto en vivo visible en los 3 pasos; moneda detectada por idioma o ubicación.'],
        ['N2', 'El usuario necesita reservar desde el celular en pocos pasos sin perder lo que ya escribió.', 'Reserva en 3 pasos con barra de progreso, botón Atrás que conserva datos.'],
        ['N3', 'El usuario necesita entender sus errores y cómo corregirlos.', 'Validación junto al campo con mensajes concretos y sugerencias (ana@gmial.com → gmail.com).'],
        ['N4', 'El usuario necesita consultar o cancelar su reserva después, desde cualquier dispositivo.', '"Mis reservas" + cuenta en Firebase sincronizada.'],
        ['N5', 'El usuario internacional necesita la app en su idioma.', '4 idiomas y 6 monedas; aviso de cookies que detecta el país con permiso.'],
        ['N6', 'Recepción necesita ver de un vistazo quién llega y quién se va hoy.', 'Pantalla Recepción con listas del día y registro de llegada.'],
    ], [1, 8.2, 6.8], 'Necesidades')

    # 5 -------------------------------------------------------------------------------
    d.h1('5. Principios UX utilizados')
    principios = [
        ('Retroalimentación', 'Presupuesto que se recalcula al instante; confirmación con confeti, referencia LMB-XXXXXX y mascota Lumi feliz; snackbars al guardar.',
         'El usuario debe saber siempre que su acción tuvo efecto.', 'Genera confianza: sabe que la reserva quedó hecha y cuánto pagará.', 'movil_confirmacion.jpg'),
        ('Prevención de errores', 'Botón Continuar solo con fechas válidas; validación de nombre, correo, teléfono y contraseña junto al campo; sugerencia de dominio; confirmación antes de cancelar.',
         'Es más barato evitar el error que corregirlo después.', 'Menos frustración y datos correctos para el hotel.', 'web_07_validaciones.jpg'),
        ('Consistencia', 'Mismos colores (turquesa/arena/sol), botones, tipografías y mensajes en web, Android e iOS; acciones principales siempre abajo a la derecha.',
         'Reduce la curva de aprendizaje entre pantallas y plataformas.', 'Lo aprendido en una pantalla sirve en todas.', 'movil_reserva_paso2.jpg'),
        ('Navegación clara', 'Barra inferior (móvil) o riel lateral (web) con la pestaña activa resaltada; pasos "Fechas · Habitación · Tus datos"; botones Atrás y cerrar (X).',
         'El usuario debe saber dónde está, qué puede hacer y cómo regresar.', 'Nunca se pierde ni queda atrapado.', 'movil_reserva_paso1.jpg'),
        ('Reconocimiento antes que memorización', 'Iconos con texto, Lumi indica qué hacer en cada paso, ejemplos en los campos, fechas con día y mes legibles.',
         'No obligar a recordar información entre pantallas.', 'Tareas más rápidas y con menos dudas.', 'movil_reserva_paso3.jpg'),
        ('Jerarquía visual y simplicidad', 'Título grande, precio destacado en turquesa, una sola acción principal por pantalla, espacios amplios.',
         'Guiar la vista hacia lo importante.', 'Encuentra el precio y el siguiente paso sin buscar.', 'movil_detalle_habitacion.jpg'),
        ('Accesibilidad y diseño centrado en el usuario', 'Tema claro/oscuro/sistema, contraste alto, áreas táctiles ≥ 48 dp, 4 idiomas, ubicación solo con permiso.',
         'Personas distintas, contextos distintos.', 'La app se adapta al usuario y no al revés.', 'movil_02_preferencias_capacidades.jpg'),
    ]
    for i, (nombre, donde, porque, beneficio, img) in enumerate(principios, 1):
        d.h2(f'5.{i} {nombre}')
        d.table(['Pregunta', 'Respuesta'], [['¿Qué principio?', nombre], ['¿Dónde está aplicado?', donde],
                                            ['¿Por qué lo usamos?', porque], ['¿Cómo beneficia al usuario?', beneficio]], [4, 12], None, 9.5)
        d.shot(img, f'Principio "{nombre}" aplicado.', 5.5)

    # 6 -------------------------------------------------------------------------------
    d.h1('6. User Flow')
    d.p('Recorrido principal de Mariana, desde que abre la app hasta ver su reserva confirmada. Incluye los puntos de '
        'decisión (cookies, validaciones) y los caminos de error con su mensaje.')
    d.diagram('15_user_flow.png', 'User Flow principal (PlantUML, diagrama de actividad).', 12)
    d.diagram('10_navegacion.png', 'Mapa de navegación completo por plataforma y rol.', 15)

    # 7 -------------------------------------------------------------------------------
    d.h1('7. Wireframes y prototipo')
    d.p('Antes de programar se diseñaron 6 pantallas de baja fidelidad (más del mínimo de 4). Cuidan jerarquía visual, '
        'distribución, alineación, espaciado, tipografía, color, consistencia, navegación, claridad de controles y '
        'accesibilidad básica. El detalle completo está en el Entregable 3 (Prototipo).')
    d.diagram('18_wireframes_todos.png', 'Wireframes: inicio, habitaciones, reserva (paso 1 y paso 3), confirmación y perfil.', 16)

    # 8 -------------------------------------------------------------------------------
    d.h1('8. Descripción de la aplicación')
    d.p('Lumbre es una sola aplicación escrita en Kotlin Multiplatform con Compose Multiplatform que se ejecuta en '
        'Android, iOS y navegador web (WebAssembly). Permite explorar habitaciones, obtener un presupuesto exacto, '
        'reservar en 3 pasos, consultar y cancelar reservas, crear una cuenta y, para el personal, operar la recepción y '
        'administrar el hotel. Los datos se guardan en Firebase (plan gratuito).')
    d.table(['Elemento', 'Detalle'], [
        ['Pantallas', '14 (Inicio, Habitaciones, Detalle, Ofertas, Reserva, Mis reservas, Llave digital, Perfil/Cuenta, Cookies y privacidad, Recepción, Administración, Superusuario, Confirmación, Avisos)'],
        ['Plataformas', 'Android (APK), iOS (Xcode) y web'],
        ['Norma de producto', 'Móvil: lo útil sobre la marcha. Web: todo, incluidos los paneles administrativos'],
        ['Idiomas y monedas', 'ES, EN, PT, FR · EUR, USD, MXN, GBP, BRL, COP'],
        ['Enlaces', f'Web: {APPWEB} · APK: {APK} · Código: {REPO}'],
    ], [3.5, 12.5], 'Ficha de la aplicación')
    d.diagram('19_arquitectura_modulos.png', 'Arquitectura por módulos (basada en gitdiagram.com).', 16)
    d.h2('8.1 Móvil frente a web')
    d.table(['', 'Móvil', 'Web'], [
        ['Se usa para', 'Reservar sobre la marcha, consultar, llave digital, recepción', 'Planear con calma y administrar'],
        ['Navegación', 'Barra inferior (5 pestañas)', 'Riel lateral con todas las pestañas del rol'],
        ['Presupuesto', 'Plegable en "Desglose"', 'Siempre visible al lado'],
    ], [3, 6.5, 6.5], 'Qué cambia según el dispositivo', 9)
    d.h2('8.2 Ventajas y desventajas de una sola app multiplataforma')
    d.pros_cons(['Misma experiencia en todos los dispositivos', 'Un cambio llega a Android, iOS y web', 'Menos código que mantener'],
                ['La web tarda más en la primera carga', 'Algunas funciones dependen de la plataforma (ubicación en iOS pendiente)'])

    # 9 -------------------------------------------------------------------------------
    d.h1('9. Capturas de las pantallas desarrolladas')
    d.h2('9.1 Versión móvil (390 × 844)')
    d.shots([('movil_cookies.jpg', 'Aviso de cookies'), ('movil_01_inicio.jpg', 'Inicio'), ('movil_detalle_habitacion.jpg', 'Detalle')], 4.6)
    d.shots([('movil_reserva_paso1.jpg', 'Paso 1: fechas'), ('movil_reserva_extras.jpg', 'Paso 2: habitación y extras'), ('movil_reserva_paso3.jpg', 'Paso 3: datos')], 4.6)
    d.shots([('movil_confirmacion.jpg', 'Confirmación'), ('movil_mis_reservas.jpg', 'Mis reservas'), ('movil_ofertas.jpg', 'Ofertas')], 4.6,
            'Recorrido completo en la vista móvil.')
    d.h2('9.2 Versión web (escritorio)')
    for f, c in (('web_03_habitaciones.jpg', 'Habitaciones con precio en la moneda detectada.'),
                 ('web_05_reserva_presupuesto.jpg', 'Reserva con presupuesto en vivo y código promocional.'),
                 ('web_09_crear_cuenta.jpg', 'Crear cuenta con medidor de fuerza de contraseña.'),
                 ('escritorio_admin_panel.jpg', 'Panel de administración (solo web): indicadores y reservas.'),
                 ('escritorio_recepcion.jpg', 'Recepción: llegadas, huéspedes en el hotel y salidas.'),
                 ('escritorio_super_parametros.jpg', 'Superusuario: parámetros del sistema sin publicar nueva versión.')):
        d.shot(f, c, 15)

    # 10 ------------------------------------------------------------------------------
    d.h1('10. Componentes gráficos utilizados')
    d.table(['Componente', 'Dónde', 'Por qué'], [
        ['Etiquetas (Text)', 'Todas las pantallas', 'Títulos, precios y ayudas con jerarquía tipográfica'],
        ['Campos de texto (OutlinedTextField)', 'Datos del huésped, cuenta, búsqueda, parámetros', 'Captura con etiqueta flotante y mensaje de error'],
        ['Botones (LumbreButton, TextButton)', 'Acciones principales y secundarias', 'Estilos Primario/Sol/Ghost con animación de rebote'],
        ['Listas (LazyColumn)', 'Habitaciones, Mis reservas, Recepción, Auditoría', 'Desplazamiento eficiente'],
        ['Select / chips de opción (FilterChip, SegmentedButton)', 'Idioma, moneda, tema, filtros de estado', 'Opciones visibles sin abrir menús'],
        ['Checkbox', 'Aceptación de privacidad y términos', 'Consentimiento explícito'],
        ['RadioButton / SegmentedButton', 'Iniciar sesión / Crear cuenta; tema', 'Elección única'],
        ['Switch', 'Disponibilidad, modo administrador, mantenimiento, cookies', 'Activar/desactivar'],
        ['Tablas', 'Panel de administración (reservas), presupuesto desglosado', 'Comparar filas y columnas'],
        ['Menús y navegación (NavigationBar, NavigationRail, menú ⋮)', 'Pestañas y acciones por fila', 'Navegación adaptable'],
        ['Imágenes (AsyncImage / recursos)', 'Hero, habitaciones, experiencias', 'Ambiente vacacional'],
        ['Diálogos (AlertDialog, DatePicker)', 'Cancelar reserva, elegir fechas', 'Confirmación y selección guiada'],
        ['Mensajes (Snackbar, avisos, Lumi)', 'Guardado, errores de red, región detectada', 'Retroalimentación'],
        ['Stepper (− valor +)', 'Huéspedes', 'Cantidad acotada sin escribir'],
    ], [5, 5.5, 5.5], 'Componentes de interfaz', 9)

    # 11 ------------------------------------------------------------------------------
    d.h1('11. Navegación e interacción')
    d.bullets([
        ('Dónde estoy', 'pestaña activa resaltada (color sol), título grande y barra de pasos en la reserva.'),
        ('Qué puedo hacer', 'una acción principal destacada por pantalla y secundarias con menor peso.'),
        ('Cómo continuar', 'botón Continuar/Confirmar fijo abajo junto al total.'),
        ('Cómo regresar o cancelar', 'botón Atrás (conserva datos), X para salir del flujo, flecha en el detalle y "Mantener" en el diálogo de cancelación.'),
        ('Adaptación', 'barra inferior en pantallas estrechas y riel lateral en anchas; contenido limitado a 1120 dp para lectura cómoda.'),
    ])

    # 12 ------------------------------------------------------------------------------
    d.h1('12. Validaciones implementadas')
    d.table(['#', 'Validación', 'Regla', 'Mensaje que ve el usuario'], [
        ['V1', 'Campo obligatorio vacío', 'Nombre y correo requeridos', 'Este campo es obligatorio.'],
        ['V2', 'Nombre con formato incorrecto', '2–80 letras, espacios, apóstrofo, punto, guion', 'Solo letras, mínimo 2.'],
        ['V3', 'Correo electrónico incorrecto', 'Formato válido, sin puntos dobles, dominio alfabético', 'Escribe un correo válido, como nombre@correo.com. + "¿Quisiste decir ana@gmail.com?"'],
        ['V4', 'Teléfono fuera de rango', '7–15 dígitos (opcional)', 'Usa entre 7 y 15 dígitos.'],
        ['V5', 'Fecha incorrecta', 'Llegada ≥ hoy; salida > llegada; ≤ 30 noches; ≤ 18 meses', 'La salida debe ser posterior a la llegada. / La llegada no puede ser anterior a hoy. / La estancia máxima es de 30 noches.'],
        ['V6', 'Cantidad fuera de rango', 'Adultos 1–6, niños 0–4, total ≤ capacidad', 'Botones − / + se desactivan en el límite; "Esta habitación admite 3 huéspedes como máximo."'],
        ['V7', 'Opción no seleccionada', 'Casilla de privacidad obligatoria', 'Necesitamos tu consentimiento. / Debes aceptar las condiciones.'],
        ['V8', 'Contraseña débil', '≥ 8, mayúscula, minúscula, número, símbolo; sin el usuario del correo', 'Mínimo 8 caracteres. / Usa mayúscula, minúscula, número y símbolo, sin espacios. + medidor de fuerza'],
        ['V9', 'Contraseñas distintas', 'Repetición igual', 'Las contraseñas no coinciden.'],
        ['V10', 'Código promocional', '4–20 mayúsculas/dígitos y activo', 'Ese código no es válido.'],
    ], [1, 3.6, 5.6, 5.8], 'Validaciones (más del mínimo de 3)', 9)
    d.shots([('web_07_validaciones.jpg', 'Validaciones en web'), ('web_09_crear_cuenta.jpg', 'Contraseña con medidor')], 7.6)

    # 13 ------------------------------------------------------------------------------
    d.h1('13. Retroalimentación del sistema')
    d.table(['Acción importante', 'Retroalimentación'], [
        ['Reserva realizada', '"¡Reserva confirmada!" + nombre, noches, habitación, referencia LMB-XXXXXX, total, confeti'],
        ['Información actualizada', 'Snackbar "Guardado" al cambiar precio, rol o parámetros'],
        ['Operación cancelada', 'Estado "Cancelada" en la tarjeta de la reserva'],
        ['Datos incorrectos', 'Campos en rojo con mensaje, Lumi preocupada'],
        ['Confirmación antes de eliminar', 'Diálogo "¿Cancelar esta reserva? Es gratis hasta 48 h antes" con Mantener / Cancelar'],
        ['Advertencia', 'Modo mantenimiento, bloqueo tras intentos fallidos con cuenta atrás'],
    ], [5, 11], 'Retroalimentación')
    d.shots([('movil_confirmacion.jpg', 'Confirmación'), ('movil_cancelar_dialogo.jpg', 'Confirmación antes de cancelar'),
             ('movil_aviso_region.jpg', 'Aviso de región')], 4.6, 'Ejemplos de retroalimentación.')

    # 14 ------------------------------------------------------------------------------
    d.h1('14. Evidencias de la prueba de usabilidad')
    d.h2('14.1 Protocolo')
    d.p('La persona participante no recibe instrucciones detalladas; solo las tareas. Se observa sin ayudar y se anota.')
    d.table(['Tarea', 'Descripción', 'Éxito si…'], [
        ['T1', 'Encuentra cuánto cuesta la Suite Deluxe 3 noches para 2 adultos, en pesos.', 'Llega al total sin ayuda'],
        ['T2', 'Reserva esa estancia con desayuno.', 'Ve la confirmación con referencia'],
        ['T3', 'Encuentra tu reserva y cancélala (sin confirmar).', 'Abre el diálogo de cancelación'],
        ['T4', 'Crea una cuenta.', 'Cuenta creada'],
    ], [1.5, 10, 4.5], 'Tareas de la prueba')
    d.p('Observaciones por registrar: ¿encontró las opciones?, ¿comprendió los botones?, ¿navegó sin ayuda?, ¿cometió '
        'errores?, ¿algo le resultó confuso?, ¿preguntó qué hacer?, ¿completó las tareas?, ¿principales dificultades?')
    d.h2('14.2 Evidencias reunidas durante el desarrollo')
    d.p('El proyecto se probó en ciclos con el responsable del producto (revisión de cada versión publicada) y con '
        'pruebas propias en 375 px y 1280 px. Estas son las observaciones reales registradas:')
    d.table(['Observación', 'Versión', 'Fuente'], [
        ['"Esa paleta es muy oscura para un hotel; añade un tema blanco."', 'App v1', 'Revisión del responsable'],
        ['"Que todos los botones funcionen."', 'App v1', 'Revisión del responsable'],
        ['"¿Cuál es la diferencia entre la versión móvil y la web?"', 'App v1', 'Pregunta del responsable'],
        ['Etiquetas de la barra inferior cortadas en pantallas estrechas', 'App v1', 'Prueba propia en 375 px'],
        ['El fondo con efecto parallax se desbordaba sobre el contenido', 'App v1', 'Prueba propia'],
        ['Título "Tu cuenta" repetido en Perfil', 'App v2', 'Prueba propia al hacer capturas'],
        ['Precios solo en euros para un público mexicano', 'Web v1', 'Revisión del responsable'],
    ], [8.5, 2, 5.5], 'Observaciones registradas')
    d.h2('14.3 Registro de la prueba con otra persona')
    d.p('Completar durante la sesión con la persona participante (nombre opcional, edad aproximada, dispositivo):')
    d.table(['Tarea', '¿Completó?', 'Tiempo', 'Errores', 'Preguntas o dudas', 'Comentario'],
            [[t, '', '', '', '', ''] for t in ('T1', 'T2', 'T3', 'T4')], [1.5, 2, 2, 2.5, 4, 4], 'Hoja de registro', 9)

    # 15 ------------------------------------------------------------------------------
    d.h1('15. Problemas encontrados')
    d.table(['#', 'Problema detectado', 'Posible causa'], [
        ['P1', 'La interfaz no transmitía "vacaciones"; se sentía pesada', 'Paleta oscura por defecto'],
        ['P2', 'Algunos botones no llevaban a ningún lado', 'Pantallas prototipo sin acción conectada'],
        ['P3', 'No quedaba claro qué se puede hacer en móvil y qué en web', 'La regla existía en el código pero no se comunicaba'],
        ['P4', 'Etiquetas de navegación cortadas', 'Textos largos para el ancho del móvil'],
        ['P5', 'Precios en euros confundían al público mexicano', 'Moneda fija'],
        ['P6', 'Título duplicado en la sección de cuenta', 'Dos componentes con el mismo encabezado'],
    ], [1, 8, 7], 'Problemas')

    # 16 ------------------------------------------------------------------------------
    d.h1('16. Mejoras realizadas y propuestas')
    d.table(['Problema', 'Solución', 'Cambio realizado'], [
        ['P1', 'Tema claro por defecto + oscuro opcional; fotos de playa, olas, efecto cristal', 'Sí (v2)'],
        ['P2', 'Revisión de cada acción; botones sin destino conectados o retirados', 'Sí (v2)'],
        ['P3', 'Sección "Qué puedes hacer aquí" en Perfil y leyenda "Llave digital en la app móvil"', 'Sí (v2)'],
        ['P4', 'Etiquetas más cortas y riel lateral en pantallas anchas', 'Sí (v1.1)'],
        ['P5', 'Detección de moneda por idioma y por ubicación con consentimiento; selector de moneda', 'Sí (v2)'],
        ['P6', 'Se eliminó el título duplicado', 'Sí (v2)'],
        ['Propuesta', 'Pagos de prueba, notificaciones de llegada, modo de alto contraste', 'Pendiente'],
    ], [2, 10, 4], 'Mejoras')

    # 17 ------------------------------------------------------------------------------
    d.h1('17. Reflexión y conclusiones')
    for q, a in (
        ('¿Qué aprendí al desarrollar la interfaz?', 'Que el diseño empieza en el usuario: definir a Mariana y sus frustraciones cambió decisiones concretas como mostrar el total siempre y validar mientras escribe.'),
        ('¿Qué decisión de UX considero más importante?', 'El presupuesto en vivo visible en los tres pasos: responde a la frustración principal (costos ocultos) y reduce el abandono.'),
        ('¿Qué problema de usabilidad encontré?', 'La falta de claridad sobre qué se puede hacer en cada plataforma y una paleta que no correspondía al contexto vacacional.'),
        ('¿Qué cambiaría si desarrollara nuevamente la aplicación?', 'Haría la prueba con usuarios externos desde los wireframes, antes de programar, y mediría tiempos por tarea desde el inicio.'),
        ('¿Diferencia entre una interfaz que "funciona" y una fácil de usar?', 'La primera ejecuta la tarea; la segunda permite que cualquiera la complete sin ayuda, entienda qué pasó y se recupere de sus errores.'),
    ):
        d.p(a, bold_prefix=q)

    # 18 ------------------------------------------------------------------------------
    return d.save()


# ======================================================================================
# E2 — CÓDIGO FUENTE
# ======================================================================================
PROPOSITO = {
    'App.kt': 'Punto común: tema, navegación con rutas tipadas, pestañas según plataforma y rol, avisos y snackbar.',
    'HotelRepository.kt': 'Fuente única de verdad: StateFlow de preferencias, catálogo, reservas, cuenta y rol; sesión, sincronización y operaciones remotas en corrutinas.',
    'Models.kt': 'Modelos de datos: Reservation, RoomConfig, PromoCode, Account, Role, Params, Prefs, Consent, AuditEntry.',
    'FirebaseApi.kt': 'Clientes REST de Firebase Authentication y Cloud Firestore con Ktor; códec de valores tipados.',
    'FirebaseConfig.kt': 'Clave de API web y id del proyecto (públicos por diseño).',
    'Mappers.kt': 'Conversión entre modelos Kotlin y campos de Firestore.',
    'Format.kt': 'Formato de moneda y fechas por idioma; conversión aproximada desde EUR.',
    'Pricing.kt': 'Cálculo del presupuesto: noches, recargo de fin de semana, extras, larga estancia, promoción, impuestos.',
    'Validation.kt': 'Reglas de validación de nombre, correo (con sugerencia), teléfono, fechas, contraseña y código.',
    'Strings.kt': 'Textos en ES, EN, PT y FR y función de verificación de traducciones faltantes.',
    'Location.kt': 'Contrato expect/actual para pedir ubicación; país por geocodificación inversa o tabla aproximada.',
    'Platform.kt': 'Capabilities: qué funciones hay según plataforma (móvil/web) y rol.',
    'Catalog.kt': 'Contenido editorial: fotos, amenidades y textos de habitaciones y experiencias.',
    'Components.kt': 'Componentes reutilizables: LumbreButton, Stepper, PhotoCard, StatusChip, AnimatedMoney, animaciones.',
    'Confetti.kt': 'Animación de confeti al confirmar.', 'Lumi.kt': 'Mascota animada con estados de ánimo y globo de texto.',
    'Vacation.kt': 'Efectos vacacionales: olas, cristal, iconos flotantes, marquesina.', 'Routes.kt': 'Rutas serializables y pestañas.',
    'AccountSection.kt': 'Formularios de inicio de sesión y registro, medidor de contraseña, cuenta iniciada.',
    'AdminScreen.kt': 'Panel web: indicadores, reservas, catálogo y promociones (según rol).',
    'BookingScreen.kt': 'Reserva en 3 pasos con presupuesto en vivo, validación y confirmación.',
    'Common.kt': 'Piezas comunes de pantallas (encabezados, avisos).', 'HomeScreen.kt': 'Inicio: hero, buscador, destacados, experiencias, opiniones.',
    'KeyScreen.kt': 'Llave digital (solo móvil).', 'OffersScreen.kt': 'Ofertas y descuentos automáticos.',
    'PrivacyScreen.kt': 'Cookies y privacidad, aviso de consentimiento y detección por ubicación.',
    'ProfileScreen.kt': 'Perfil, cuenta, preferencias y "Qué puedes hacer aquí".', 'ReceptionScreen.kt': 'Recepción del día (STAFF+).',
    'RoomDetailScreen.kt': 'Detalle de habitación.', 'RoomsScreen.kt': 'Listado de habitaciones.',
    'SuperAdminScreen.kt': 'Panel de superusuario: usuarios y roles, parámetros, auditoría y seguridad.', 'TripsScreen.kt': 'Mis reservas y cancelación.',
    'Theme.kt': 'Colores, tipografía (Playfair + Inter) y formas; tema claro/oscuro.', 'PricingTest.kt': '6 pruebas del presupuesto.',
    'ValidationTest.kt': '8 pruebas de validación, formato, detección de país, roles, traducciones y códec.',
    'MainActivity.kt': 'Punto de entrada Android.', 'main.kt': 'Punto de entrada web (Wasm).', 'MainViewController.kt': 'Punto de entrada iOS.',
    'Location.android.kt': 'Ubicación en Android (permiso y LocationManager).', 'Location.wasmJs.kt': 'Ubicación en navegador (navigator.geolocation).',
    'Location.ios.kt': 'Ubicación en iOS (pendiente: devuelve no disponible).',
}


def inventario():
    rows = []
    base = os.path.join(ROOT, 'app')
    for dp, _, fs in os.walk(base):
        if any(x in dp for x in ('build', '.gradle', 'kotlin-js-store', 'iosApp.xcodeproj', '.idea')):
            continue
        for f in fs:
            if f.endswith('.kt'):
                p = os.path.join(dp, f)
                n = sum(1 for _ in open(p, encoding='utf-8'))
                rel = os.path.relpath(p, base).replace(os.sep, '/')
                rel = rel.replace('shared/src/', '').replace('kotlin/com/lumbre/hotel/', '')
                rows.append([rel, str(n), PROPOSITO.get(f, '—')])
    rows.sort()
    return rows


def e2():
    d = Doc('U1/U1_E2_Codigo_Fuente.docx', U, 'Entregable 2 · Código fuente', 'Código fuente del proyecto',
            'Estructura, instalación, explicación del código y preparación para la defensa')
    d.toc(['Entrega', 'Tecnologías', 'Estructura de carpetas', 'Inventario de archivos', 'Cómo ejecutar',
           'Código clave explicado', 'Pruebas', 'Preparación para la defensa'])
    d.h1('1. Entrega')
    d.table(['Elemento', 'Valor'], [
        ['Archivo comprimido', f'{ZIP} (en la carpeta de Drive de la Unidad 1)'], ['Repositorio', REPO],
        ['Excluido del ZIP', 'build/, .gradle/, .idea/, kotlin-js-store, local.properties, node_modules y binarios generados'],
        ['Aplicación publicada', f'{APPWEB} · APK: {APK}'],
    ], [4, 12], 'Entrega')
    d.h1('2. Tecnologías')
    d.bullets(['Kotlin 2.4 · Kotlin Multiplatform', 'Compose Multiplatform 1.11 + Material 3', 'Navigation Compose (rutas tipadas)',
               'Ktor 3.5 (HTTP) · kotlinx-serialization · kotlinx-datetime · multiplatform-settings',
               'Firebase Authentication + Cloud Firestore (REST)', 'Gradle 9.4 · AGP 9.2 · GitHub Actions + Pages'])
    d.h1('3. Estructura de carpetas')
    d.code('''hotel-lumbre/
├─ index.html · css/ · js/            Página web informativa (HTML, CSS, JavaScript)
├─ app/                               Aplicación Kotlin Multiplatform
│  ├─ shared/src/commonMain/…         Código común (UI, dominio, datos, i18n)
│  ├─ shared/src/androidMain|iosMain|wasmJsMain/   Implementaciones por plataforma
│  ├─ shared/src/commonTest/          Pruebas unitarias
│  ├─ androidApp/ · iosApp/ · webApp/ Puntos de entrada
│  └─ firebase/firestore.rules        Reglas de seguridad
├─ docs/                              Diagramas, capturas, generador de documentos, SQL
└─ .github/workflows/pages.yml        Compilación y publicación automática''')
    d.diagram('04_arquitectura.png', 'Arquitectura por capas.', 15)
    d.h1('4. Inventario de archivos Kotlin')
    rows = inventario()
    d.table(['Archivo', 'Líneas', 'Propósito'], rows, [6.5, 1.4, 8.1], f'Inventario ({len(rows)} archivos, {sum(int(r[1]) for r in rows)} líneas)', 8)
    d.h1('5. Cómo ejecutar')
    d.code('''git clone https://github.com/JanCarliux24/hotel-lumbre
cd hotel-lumbre/app
./gradlew :webApp:wasmJsBrowserDevelopmentRun     # web en el navegador
./gradlew :androidApp:assembleDebug                # APK en androidApp/build/outputs/apk/debug
./gradlew :shared:testAndroidHostTest              # 14 pruebas unitarias
# iOS: abrir iosApp/iosApp.xcodeproj en Xcode (macOS)''', 'Comandos (requiere JDK 21 de Android Studio).')
    d.h1('6. Código clave explicado')
    d.h2('6.1 Validación con mensajes comprensibles')
    d.code('''fun email(value: String): K? {
    val v = value.trim()
    if (v.isEmpty()) return K.E_REQUIRED      // "Este campo es obligatorio."
    val at = v.lastIndexOf('@')
    if (at <= 0 || v.length > 254 || at > 64) return K.E_EMAIL
    val local = v.substring(0, at)
    val tld = v.substringAfterLast('.')
    if (!emailRegex.matches(v) || ".." in v || local.startsWith('.') || local.endsWith('.') ||
        tld.length < 2 || !tld.all { it.isLetter() }
    ) return K.E_EMAIL                        // "Escribe un correo válido, como nombre@correo.com."
    return null                               // null = válido
}''', 'domain/Validation.kt — devuelve una clave de texto traducible en vez de un código de error.')
    d.h2('6.2 Presupuesto')
    d.code('''for (i in 0 until nights) {
    val day = checkIn.plus(i, DateTimeUnit.DAY).dayOfWeek
    base += room.nightlyEur
    if (day == DayOfWeek.FRIDAY || day == DayOfWeek.SATURDAY) weekend += room.nightlyEur * weekendRate
}''', 'domain/Pricing.kt — recargo del 15 % solo en noches de viernes y sábado.')
    d.h2('6.3 Estado reactivo y concurrencia')
    d.code('''private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
private fun remote(block: suspend () -> Unit) {
    if (!cloud || _account.value == null) return
    scope.launch {
        try { block() } catch (e: Throwable) { _events.tryEmit(mapError(e)); refreshAll() }
    }
}''', 'data/HotelRepository.kt — la UI se actualiza al instante y la escritura en la nube ocurre en segundo plano.')
    d.diagram('14_concurrencia.png', 'Flujo síncrono/asíncrono al reservar.', 15)
    d.h2('6.4 Navegación tipada')
    d.code('''@Serializable data class BookingRoute(val room: String? = null, val checkIn: String? = null,
    val checkOut: String? = null, val guests: Int = 2, val promo: String? = null)
navController.navigate(BookingRoute(promo = "LUMBRE10"))''', 'ui/navigation/Routes.kt')
    d.h1('7. Pruebas')
    d.p('14 pruebas unitarias en commonTest (6 de presupuesto y 8 de validación y utilidades), todas en verde. '
        'Ejemplo: 3 noches entre semana en Suite Deluxe a 190 € = 627 € (570 + 10 % de impuestos).')
    d.h1('8. Preparación para la defensa')
    d.table(['Pregunta posible', 'Respuesta'], [
        ['¿Por qué colocaste el botón principal abajo?', 'Zona del pulgar en móvil y consistente en todas las pantallas; junto al total para decidir con la información a la vista.'],
        ['¿Qué principio UX aplicas en el presupuesto?', 'Retroalimentación y visibilidad del estado del sistema.'],
        ['¿Qué ocurre si el usuario introduce información incorrecta?', 'El campo se marca en rojo con un mensaje concreto; no se puede confirmar hasta corregirlo; si hay un error típico de dominio se sugiere el correcto.'],
        ['¿Cómo das retroalimentación?', 'Presupuesto en vivo, Lumi, snackbars, confirmación con referencia y confeti, diálogos antes de acciones destructivas.'],
        ['¿Qué problema encontraste en la prueba?', 'La paleta oscura y la falta de claridad entre móvil y web (ver §15 del Entregable 1).'],
        ['¿Por qué seleccionaste ese componente?', 'Stepper para cantidades acotadas, chips para opciones visibles, diálogo para confirmar acciones irreversibles.'],
        ['¿Cómo funciona esta sección del código?', 'Ver §6: validación pura, presupuesto puro y repositorio reactivo con corrutinas.'],
    ], [5.5, 10.5], 'Defensa')
    return d.save()


# ======================================================================================
# E3 — PROTOTIPO
# ======================================================================================
def e3():
    d = Doc('U1/U1_E3_Prototipo.docx', U, 'Entregable 3 · Prototipo', 'Prototipo y sistema de diseño',
            'Wireframes, guía visual y correspondencia entre prototipo e implementación')
    d.toc(['Herramienta y alcance', 'Wireframes pantalla por pantalla', 'Sistema de diseño', 'User Flow y navegación',
           'Correspondencia prototipo → implementación'])
    d.h1('1. Herramienta y alcance')
    d.p('Los wireframes se elaboraron con PlantUML Salt (texto que genera bocetos), una herramienta gratuita que permite '
        'versionar el prototipo junto con el código. Se diseñaron 6 pantallas (mínimo pedido: 4).')
    d.pros_cons(['Gratis y versionado junto al código', 'Cambios rápidos en texto', 'Mismo estilo en todos los bocetos'],
                ['Menos libertad visual que Figma', 'No es interactivo (no se puede "hacer clic")'], 'Prototipar con PlantUML Salt')
    d.h1('2. Wireframes pantalla por pantalla')
    wf = [
        ('18_wf1_inicio.png', 'Pantalla 1 · Inicio', 'Buscador de fechas y huéspedes sobre la foto del hotel; destacados; barra inferior.', 'Jerarquía: título grande y botón "Ver precios" como acción única.'),
        ('18_wf2_habitaciones.png', 'Pantalla 2 · Habitaciones', 'Tarjetas con foto, capacidad, superficie, valoración y precio por noche.', 'Distribución en lista; precio alineado a la derecha para comparar.'),
        ('18_wf3_reserva_fechas.png', 'Pantalla 3 · Reserva paso 1 (captura)', 'Fechas, huéspedes y presupuesto desglosado.', 'Barra de pasos y mascota que guía.'),
        ('18_wf4_reserva_datos.png', 'Pantalla 4 · Reserva paso 3 (validación)', 'Datos del huésped con errores en rojo y sugerencia de correo.', 'Mensajes junto al campo; Atrás y Confirmar.'),
        ('18_wf5_confirmacion.png', 'Pantalla 5 · Confirmación', 'Referencia, resumen y acciones siguientes.', 'Retroalimentación clara y cierre del flujo.'),
        ('18_wf6_perfil_cuenta.png', 'Pantalla 6 · Perfil', 'Cuenta, privacidad, preferencias y capacidades por plataforma.', 'Agrupación por secciones con títulos.'),
    ]
    for img, t, desc, dec in wf:
        d.h2(t)
        d.diagram(img, t, 7.5)
        d.p(desc, bold_prefix='Contenido:')
        d.p(dec, bold_prefix='Decisión de diseño:')
    d.h1('3. Sistema de diseño')
    d.table(['Token', 'Valor', 'Uso'], [
        ['Turquesa (primario)', '#0A7C86', 'Botones principales, enlaces, pestaña activa del contenido'],
        ['Azul noche', '#16313A', 'Títulos y texto principal'],
        ['Sol', '#F4A63A', 'Acción de confirmar, pestaña activa de navegación'],
        ['Arena', '#FFF4E2 / #F3EDE3', 'Fondos de globo, chips seleccionados'],
        ['Error', '#B3261E', 'Mensajes de validación'],
        ['Éxito', '#207A4F', 'Confirmación, estado "Confirmada"'],
        ['Tipografía de títulos', 'Playfair Display', 'Encabezados con carácter vacacional'],
        ['Tipografía de texto', 'Inter', 'Lectura cómoda en pantallas pequeñas'],
        ['Espaciado', 'Múltiplos de 4 dp (8, 12, 16, 24)', 'Ritmo vertical constante'],
        ['Radios', '14–28 dp', 'Tarjetas y botones redondeados'],
        ['Área táctil mínima', '48 dp', 'Accesibilidad'],
    ], [4, 4.5, 7.5], 'Tokens de diseño')
    d.h1('4. User Flow y navegación')
    d.diagram('15_user_flow.png', 'User Flow.', 11)
    d.diagram('10_navegacion.png', 'Mapa de navegación.', 15)
    d.h1('5. Correspondencia prototipo → implementación')
    d.p('El diseño desarrollado conserva la relación con el prototipo; las diferencias son mejoras surgidas en pruebas.')
    pares = [
        ('18_wf1_inicio.png', 'movil_01_inicio.jpg', 'Se conservó la estructura; se añadió la mascota y el aviso de región.'),
        ('18_wf3_reserva_fechas.png', 'movil_reserva_paso1.jpg', 'El desglose se movió a un panel "Desglose" plegable para ganar espacio en móvil.'),
        ('18_wf4_reserva_datos.png', 'web_07_validaciones.jpg', 'Igual que el prototipo: errores en rojo y sugerencia de correo.'),
        ('18_wf5_confirmacion.png', 'movil_confirmacion.jpg', 'Se añadió el nombre del huésped y el confeti.'),
        ('18_wf6_perfil_cuenta.png', 'movil_02_preferencias_capacidades.jpg', 'Se añadieron moneda como chips y la sección de capacidades.'),
    ]
    from docgen import DIAG, SHOTS
    import docx.shared as S
    for wfi, cap, nota in pares:
        t = d.d.add_table(rows=1, cols=2)
        for i, path in enumerate((os.path.join(DIAG, wfi), os.path.join(SHOTS, cap))):
            c = t.rows[0].cells[i]; c.text = ''
            if os.path.exists(path):
                c.paragraphs[0].add_run().add_picture(path, width=S.Cm(6.5 if i == 0 else 5))
        d.p(nota, bold_prefix='Prototipo (izq.) vs. implementación (der.):')
    return d.save()


ALL = [e1, e2, e3]
