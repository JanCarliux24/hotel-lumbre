"""Entregables de la Unidad 2 (6 documentos)."""
import os
from docgen import Doc, WEB, APPWEB, APK, REPO, ROOT

U = 'Unidad 2 · Librerías, componentes y su aplicación'


# ======================================================================================
# E1. ESPECIFICACIONES
# ======================================================================================
def e1():
    d = Doc('U2_Librerias/U2_E1_Especificaciones.docx', U, 'Entregable 1', 'Especificaciones del sistema',
            'Requisitos funcionales y no funcionales, actores, casos de uso, reglas y criterios de aceptación')
    d.toc(['Introducción y alcance', 'Visión del producto', 'Actores y roles', 'Plataformas y norma "móvil útil / web completa"',
           'Requisitos funcionales', 'Requisitos no funcionales', 'Reglas de negocio y parámetros', 'Validaciones de entrada',
           'Seguridad', 'Cookies, ubicación, idioma y moneda', 'Casos de uso', 'Arquitectura', 'Navegación', 'Criterios de aceptación', 'Glosario', 'Modelo de clases y estados', 'Seguridad y manejo de datos', 'Vistas móvil y web', 'Criterios TAP'])

    d.h1('1. Introducción y alcance')
    d.p('Este documento especifica el sistema de reservas de Lumbre Hotel & Spa: una sola aplicación escrita con Kotlin '
        'Multiplatform y Compose Multiplatform que se ejecuta en Android, iOS y navegador web (Kotlin/Wasm), conectada a '
        'Firebase (Authentication y Cloud Firestore, plan gratuito). Incluye además una página web informativa estática.')
    d.table(['Elemento', 'Enlace'], [
        ['Página web del hotel', WEB], ['Aplicación web', APPWEB], ['APK Android', APK], ['Código fuente', REPO],
    ], [4, 12], 'Entregables publicados')
    d.p('Fuera de alcance en esta versión: pagos en línea, asignación de número de habitación física, facturación '
        'electrónica e integración con agencias externas.')

    d.h1('2. Visión del producto')
    d.p('Que cualquier huésped, desde cualquier país y dispositivo, pueda descubrir el hotel, ver precios en su moneda e '
        'idioma, obtener un presupuesto exacto y reservar en menos de un minuto; y que el personal del hotel gestione '
        'reservas, catálogo y usuarios con permisos claros y con todo registrado.')
    d.bullets([
        ('Experiencia', 'animaciones suaves (transiciones compartidas, rebotes, confeti), mascota "Lumi" que guía, tema claro por defecto con oscuro opcional.'),
        ('Una sola base de código', 'el 100 % de la lógica y de la interfaz vive en el módulo shared; cada plataforma solo aporta un punto de entrada.'),
        ('Sin costo', 'todos los servicios usados tienen plan gratuito.'),
    ])

    d.h1('3. Actores y roles')
    d.table(['Rol', 'Nivel', 'Quién es', 'Qué puede hacer'], [
        ['Visitante', '—', 'Sin cuenta', 'Explorar, presupuestar, reservar (se guarda en su dispositivo).'],
        ['GUEST', '0', 'Huésped registrado', 'Lo anterior + reservas y preferencias sincronizadas en la nube, cancelar, llave digital (móvil).'],
        ['STAFF', '1', 'Recepción', 'Recepción del día (llegadas, en el hotel, salidas), registrar llegada, cancelar.'],
        ['ADMIN', '2', 'Administración', 'Precios, disponibilidad, promociones e indicadores (web).'],
        ['SUPERADMIN', '3', 'Dirección / TI', 'Usuarios y roles, bloqueo de cuentas, parámetros del sistema, auditoría y estado de seguridad (web).'],
    ], [2.6, 1.3, 3.3, 8.8], 'Roles del sistema')
    d.diagram('05_casos_uso.png', 'Diagrama de casos de uso por actor.', 15.5)

    d.h1('4. Plataformas y norma "móvil útil / web completa"')
    d.p('La misma aplicación decide qué funciones mostrar según la plataforma (objeto Capabilities) y el rol. En móvil se '
        'priorizan las tareas rápidas que se hacen de pie o de viaje; en la web, con pantalla grande y teclado, están todas.')
    d.table(['Función', 'Android / iOS', 'Web'], [
        ['Explorar, presupuestar, reservar, ofertas', 'Sí', 'Sí'],
        ['Cuenta, mis reservas, cancelar, preferencias', 'Sí', 'Sí'],
        ['Cookies y privacidad, detección por ubicación', 'Sí', 'Sí'],
        ['Llave digital de la habitación', 'Sí (solo móvil)', 'No'],
        ['Recepción del día (STAFF+)', 'Sí', 'Sí'],
        ['Panel administrativo: reservas e indicadores (STAFF+)', 'No', 'Sí'],
        ['Catálogo: precios, disponibilidad, promociones (ADMIN+)', 'No', 'Sí'],
        ['Panel de superusuario (SUPERADMIN)', 'No', 'Sí'],
    ], [9, 3.5, 3.5], 'Funciones por plataforma')

    d.h1('5. Requisitos funcionales')
    rf = [
        ['RF-01', 'Mostrar inicio con buscador de fechas y huéspedes, habitaciones destacadas, experiencias y opiniones.', 'Alta'],
        ['RF-02', 'Listar los 3 tipos de habitación con foto, capacidad, superficie, valoración y precio en la moneda elegida.', 'Alta'],
        ['RF-03', 'Mostrar el detalle de una habitación con galería, amenidades y botón Reservar.', 'Alta'],
        ['RF-04', 'Reservar en 3 pasos (fechas y huéspedes → habitación y extras → datos) con presupuesto en vivo.', 'Alta'],
        ['RF-05', 'Calcular presupuesto: noches, recargo de fin de semana, extras por unidad, descuento por larga estancia, código promocional e impuestos.', 'Alta'],
        ['RF-06', 'Generar referencia única LMB-XXXXXX y mostrar confirmación con confeti.', 'Alta'],
        ['RF-07', 'Listar "Mis reservas" (próximas, pasadas, canceladas) y permitir cancelar.', 'Alta'],
        ['RF-08', 'Pestaña Ofertas con códigos activos y descuentos automáticos; "Usar en mi reserva" precarga el código.', 'Media'],
        ['RF-09', 'Crear cuenta, iniciar sesión, cerrar sesión, recuperar contraseña, verificar correo, cambiar contraseña y eliminar cuenta.', 'Alta'],
        ['RF-10', 'Sincronizar perfil, preferencias y reservas al iniciar sesión en cualquier dispositivo; subir reservas locales previas.', 'Alta'],
        ['RF-11', 'Pestaña Cookies y privacidad: categorías (necesarias, preferencias, ubicación), guardar elección, borrar mis datos.', 'Alta'],
        ['RF-12', 'Con permiso, pedir la ubicación aproximada y fijar idioma y moneda del país detectado.', 'Alta'],
        ['RF-13', 'Recepción: listas de llegadas, en el hotel y salidas de hoy; registrar llegada; búsqueda por referencia o nombre.', 'Media'],
        ['RF-14', 'Panel administrativo web: reservas con filtros e indicadores (ingresos, ticket medio, activas).', 'Media'],
        ['RF-15', 'Catálogo web: editar precio y disponibilidad, crear/editar/eliminar promociones.', 'Media'],
        ['RF-16', 'Panel de superusuario: cambiar roles, bloquear cuentas, editar parámetros, ver auditoría y estado de seguridad.', 'Alta'],
        ['RF-17', 'Llave digital (móvil) para reservas confirmadas o en curso.', 'Baja'],
        ['RF-18', 'Cambiar idioma (ES, EN, PT, FR), moneda (EUR, USD, MXN, GBP, BRL, COP) y tema (claro, oscuro, sistema).', 'Alta'],
    ]
    d.table(['ID', 'Descripción', 'Prioridad'], rf, [1.6, 12.4, 2], 'Requisitos funcionales', 9)

    d.h1('6. Requisitos no funcionales')
    d.table(['ID', 'Categoría', 'Requisito', 'Cómo se verifica'], [
        ['RNF-01', 'Portabilidad', 'Un solo código para Android (minSdk 26), iOS y navegadores con WebAssembly GC.', 'Builds de las 3 plataformas en CI.'],
        ['RNF-02', 'Usabilidad', 'Reserva completa en ≤ 3 pasos y < 60 s; mensajes de error junto al campo y en lenguaje claro.', 'Pruebas con usuarios (E5).'],
        ['RNF-03', 'Diseño adaptable', 'Barra inferior en pantallas estrechas y riel lateral en anchas; contenido limitado a 1120 dp.', 'Capturas móvil/escritorio.'],
        ['RNF-04', 'Rendimiento', 'Animaciones a 60 fps; primera carga web < 5 s en banda ancha.', 'Medición en navegador.'],
        ['RNF-05', 'Seguridad', 'Reglas de Firestore en servidor, tokens de 1 h, bloqueo por intentos, sin contraseñas en la app.', 'Pruebas de reglas y de interfaz.'],
        ['RNF-06', 'Privacidad', 'Consentimiento previo; ubicación redondeada (~11 km) y no almacenada; borrar mis datos.', 'Revisión del flujo de cookies.'],
        ['RNF-07', 'Disponibilidad', 'Funciona sin conexión con datos locales; sincroniza al volver.', 'Prueba en modo avión.'],
        ['RNF-08', 'Mantenibilidad', 'Capas separadas (ui, domain, data, platform, i18n); pruebas unitarias de dominio.', '14 pruebas en verde.'],
        ['RNF-09', 'Internacionalización', 'Toda cadena visible en 4 idiomas; prueba automática que detecta traducciones faltantes.', 'missingTranslations() vacío.'],
        ['RNF-10', 'Costo', '0 € de operación.', 'Firebase Spark + GitHub Pages.'],
    ], [1.6, 2.6, 7, 4.8], 'Requisitos no funcionales', 9)

    d.h1('7. Reglas de negocio y parámetros')
    d.p('Los valores marcados con * son parámetros editables por el superusuario sin publicar una nueva versión.')
    d.table(['Regla', 'Valor'], [
        ['Impuestos*', '10 % sobre el subtotal'],
        ['Recargo de viernes y sábado*', '+15 % por noche'],
        ['Descuento por larga estancia*', '−10 % desde 7 noches*'],
        ['Noches máximas por reserva*', '30'],
        ['Antelación máxima*', '18 meses'],
        ['Espera entre reservas*', '20 s (anti-abuso)'],
        ['Intentos de inicio de sesión* / bloqueo*', '5 intentos / 60 s'],
        ['Longitud mínima de contraseña*', '8'],
        ['Modo mantenimiento*', 'Pausa reservas de huéspedes con mensaje'],
        ['Extras', 'Desayuno 18 €/persona y noche (niños 50 %), Spa 45 €/adulto, Traslado 60 €/estancia, Parking 15 €/noche, Salida tardía 30 €/estancia'],
        ['Capacidad', 'Estándar 2, Deluxe 3, Ático 6 huéspedes'],
    ], [6.5, 9.5], 'Reglas y parámetros')

    d.h1('8. Validaciones de entrada')
    d.table(['Campo', 'Regla', 'Mensaje (ES)'], [
        ['Nombre', '2–80 caracteres, letras (con acentos), espacios, apóstrofo, punto y guion.', 'Solo letras, mínimo 2.'],
        ['Correo', 'Formato RFC simplificado, sin puntos dobles, TLD alfabético; sugerencia de dominio (gmial → gmail).', '¿Quisiste decir ana@gmail.com?'],
        ['Teléfono', 'Opcional; 7–15 dígitos; admite + ( ) . - y espacios.', 'Usa entre 7 y 15 dígitos.'],
        ['Fechas', 'Llegada ≥ hoy; salida > llegada; ≤ 30 noches; ≤ 18 meses.', 'La salida debe ser posterior a la llegada.'],
        ['Huéspedes', 'Adultos 1–6, niños 0–4, total ≤ capacidad.', 'Esta habitación admite hasta N.'],
        ['Contraseña', '≥ 8, mayúscula, minúscula, número y símbolo; no contener el usuario del correo; medidor de fuerza 0–4.', 'Mínimo 8 caracteres. / Usa mayúscula, minúscula, número y símbolo, sin espacios.'],
        ['Repetir contraseña', 'Igual a la anterior.', 'Las contraseñas no coinciden.'],
        ['Código promocional', '4–20 mayúsculas o dígitos y existir activo.', 'Ese código no es válido.'],
        ['Términos', 'Casilla obligatoria al reservar y al crear cuenta.', 'Necesitamos tu consentimiento. / Debes aceptar las condiciones.'],
    ], [3, 8, 5], 'Validaciones')
    d.shot('web_07_validaciones.jpg', 'Validaciones en vivo en el paso "Tus datos" (nombre, sugerencia de correo, teléfono y casilla).')

    d.h1('9. Seguridad')
    d.bullets([
        'Autenticación con Firebase Authentication; la app nunca guarda contraseñas, solo el token de renovación.',
        'Token de acceso de 1 hora renovado automáticamente; cierre de sesión borra tokens locales.',
        'Bloqueo temporal tras 5 intentos fallidos (parametrizable) y mensajes que no revelan si el correo existe.',
        'Reglas de Firestore: cada usuario solo lee y escribe lo suyo; el rol solo lo cambia el superusuario; el usuario nace como GUEST.',
        'Validación en dos capas: cliente (experiencia) y servidor (reglas), con los mismos rangos.',
        'Auditoría inmutable de acciones administrativas.',
        'Comprobación de rol en cada pantalla protegida (GuardNotice) además de ocultar pestañas.',
        'Cooldown entre reservas y referencias imposibles de adivinar (alfabeto sin 0/O/1/I).',
    ])

    d.h1('10. Cookies, ubicación, idioma y moneda')
    d.p('Al abrir por primera vez aparece un aviso con tres opciones: Aceptar todo, Solo necesarias o Configurar. La categoría '
        '"Ubicación" pide permiso al sistema (navegador o Android) solo cuando el usuario la activa; las coordenadas se redondean '
        'a 1 decimal (~11 km) antes de consultar el país, y si no hay conexión se usa una tabla local de regiones aproximadas. '
        'Con el país se fijan idioma (p. ej. México → ES) y moneda (México → MXN). Si el usuario rechaza, se usa el idioma del dispositivo.')
    d.shot('web_01_cookies.jpg', 'Aviso de cookies y ubicación en el primer uso.')
    d.shot('web_02_privacidad.jpg', 'Pestaña Cookies y privacidad con las tres categorías y la detección por ubicación.')

    d.h1('11. Casos de uso')
    cu = [
        ('CU-01 Reservar estancia', 'Visitante / GUEST', 'Elegir fechas y huéspedes → elegir habitación y extras → introducir datos y aceptar → confirmar.',
         'Fechas inválidas: se bloquea "Continuar". Mantenimiento: aviso y no se reserva. Cooldown: se pide esperar.'),
        ('CU-02 Crear cuenta', 'Visitante', 'Nombre, teléfono, correo, contraseña doble y términos → Crear cuenta → correo de verificación.',
         'Correo ya registrado: mensaje claro. Contraseña débil: reglas visibles.'),
        ('CU-03 Iniciar sesión en otro dispositivo', 'GUEST', 'Correo y contraseña → se descargan perfil, preferencias y reservas.',
         '5 fallos: bloqueo temporal con cuenta atrás.'),
        ('CU-04 Registrar llegada', 'STAFF', 'Recepción → Llegadas de hoy → Registrar llegada.', 'Sin permiso: aviso de acceso restringido.'),
        ('CU-05 Cambiar precio', 'ADMIN', 'Panel web → Catálogo → ajustar precio → se guarda en la nube y en auditoría.', 'Fuera de rango: lo rechaza la regla.'),
        ('CU-06 Asignar rol', 'SUPERADMIN', 'Superusuario → Usuarios → elegir rol.', 'No puede cambiar su propio rol.'),
    ]
    for t, actor, flujo, alt in cu:
        d.h3(t)
        d.table(['Actor', 'Flujo principal', 'Flujos alternos'], [[actor, flujo, alt]], [3, 7, 6], None, 9)
    d.diagram('06_secuencia_reserva.png', 'Secuencia del caso de uso "Reservar estancia".', 15.5)

    d.h1('12. Arquitectura')
    d.diagram('04_arquitectura.png', 'Arquitectura por capas de la aplicación multiplataforma.', 15.5)
    d.diagram('08_despliegue.png', 'Diagrama de despliegue (GitHub Pages, APK, Firebase).', 15.5)

    d.h1('13. Navegación')
    d.diagram('10_navegacion.png', 'Mapa de navegación con pestañas según plataforma y rol.', 15.5)

    d.h1('14. Criterios de aceptación')
    d.table(['Requisito', 'Criterio (Dado / Cuando / Entonces)'], [
        ['RF-05', 'Dado Suite Deluxe a 190 € del martes 1 al viernes 4 de diciembre para 2 adultos, cuando se calcula, entonces el total es 627 € (570 + 10 %).'],
        ['RF-05', 'Dado viernes 4 a domingo 6, entonces el recargo de fin de semana es 57 € (2 × 190 × 15 %).'],
        ['RF-09', 'Dada la contraseña "abcdefgh1", entonces se rechaza por no cumplir las reglas.'],
        ['RF-12', 'Dadas coordenadas de Morelia (19.7, −101.2) sin conexión, entonces el país es MX y la moneda MXN.'],
        ['RF-16', 'Dado un STAFF, cuando intenta cambiar el rol de otro usuario en Firestore, entonces la regla lo rechaza (403).'],
        ['RNF-09', 'Dada cualquier clave de texto, entonces existe en ES, EN, PT y FR (prueba automática).'],
    ], [2.5, 13.5], 'Criterios de aceptación verificados con pruebas unitarias')

    d.h1('15. Glosario')
    d.table(['Término', 'Definición'], [
        ['KMP', 'Kotlin Multiplatform: compartir código Kotlin entre plataformas.'],
        ['Compose Multiplatform', 'Framework de interfaz declarativa de JetBrains para Android, iOS, escritorio y web.'],
        ['Wasm', 'WebAssembly: formato binario que ejecuta la app Kotlin en el navegador.'],
        ['Firestore', 'Base de datos NoSQL documental de Firebase.'],
        ['Regla de seguridad', 'Condición evaluada por Firestore en el servidor antes de aceptar una lectura o escritura.'],
        ['Cooldown', 'Tiempo mínimo entre dos acciones iguales.'],
    ], [4, 12], 'Glosario')
    d.h1('16. Modelo de clases y estados')
    d.diagram('16_clases_dominio.png', 'Diagrama de clases del dominio (código común).', 16)
    d.diagram('17_estados_reserva.png', 'Ciclo de vida de una reserva.', 12)
    d.diagram('19_arquitectura_modulos.png', 'Arquitectura por módulos (basada en gitdiagram.com).', 16)
    d.diagram('14_concurrencia.png', 'Trabajo síncrono y asíncrono sin bloquear la interfaz.', 15)
    d.h1('17. Seguridad y manejo de datos (detalle)')
    d.h2('17.1 Qué datos se guardan y dónde')
    d.table(['Dato', 'Dónde se guarda', 'Quién puede verlo', 'Para qué se usa'], [
        ['Contraseña', 'Solo en Firebase Authentication (cifrada); nunca en la app ni en la base de datos', 'Nadie, ni el hotel', 'Iniciar sesión'],
        ['Nombre, correo, teléfono', 'Firestore users/{uid}', 'La propia persona y el superusuario', 'Cuenta y contacto'],
        ['Preferencias (idioma, moneda, tema)', 'Firestore y el dispositivo', 'La propia persona', 'Mostrar la app como le gusta'],
        ['Reservas', 'Firestore reservations y copia en el dispositivo', 'Su dueño y el personal (STAFF+)', 'Estancia, recepción, indicadores'],
        ['Token de sesión', 'Dispositivo (se borra al cerrar sesión)', 'Solo la app', 'Mantener la sesión 1 h y renovarla'],
        ['Ubicación', 'No se guarda: se redondea (~11 km) y solo se usa para saber el país', 'Nadie', 'Elegir idioma y moneda'],
        ['Auditoría', 'Firestore audit', 'Solo el superusuario', 'Saber quién cambió qué'],
    ], [3.3, 5, 3.6, 4.1], 'Inventario de datos', 8.5)
    d.h2('17.2 Ciclo de vida de los datos')
    d.bullets([('Recolección', 'solo lo necesario y con consentimiento (casilla obligatoria y aviso de cookies).'),
               ('Uso', 'cada dato tiene una finalidad concreta (tabla anterior).'),
               ('Actualización', 'la persona edita su perfil; el personal solo cambia estados de reserva.'),
               ('Conservación', 'las reservas canceladas se conservan como historial; la auditoría no se borra.'),
               ('Eliminación', '"Borrar mis datos" limpia el dispositivo y "Eliminar cuenta" borra la cuenta y el perfil.')])
    d.h2('17.3 Amenazas y cómo se controlan')
    d.table(['Amenaza', 'Ejemplo', 'Control aplicado'], [
        ['Suplantación', 'Alguien intenta entrar con la cuenta de otra persona', 'Contraseña robusta, bloqueo tras 5 intentos, mensajes que no revelan si el correo existe'],
        ['Escalada de privilegios', 'Un huésped intenta darse rol de administrador', 'Regla: solo SUPERADMIN cambia roles; todo usuario nace GUEST'],
        ['Manipulación de datos', 'Alterar el precio de una reserva desde el navegador', 'Reglas en el servidor validan campos y rangos; el dueño solo puede cancelar'],
        ['Lectura indebida', 'Ver reservas de otros huéspedes', 'Regla: cada quien lee lo suyo; listado completo solo para STAFF+'],
        ['Abuso / spam', 'Crear cientos de reservas falsas', 'Espera entre reservas (cooldown), referencias imposibles de adivinar'],
        ['Robo de sesión', 'Copiar el token de un dispositivo', 'Token de 1 h, HTTPS en todas las conexiones, cierre de sesión borra tokens'],
        ['Código malicioso en la web', 'Inyectar scripts', 'Política de contenido (CSP) y Compose renderiza texto, no HTML'],
        ['Pérdida de datos', 'Error humano borra un catálogo', 'Auditoría para rastrear; exportación manual periódica (el plan gratuito no incluye respaldos)'],
        ['Clave de API visible', 'Alguien ve la clave en el código web', 'Es pública por diseño en Firebase; la protección real está en las reglas'],
    ], [3.2, 5, 7.8], 'Amenazas y controles', 8.5)
    d.h2('17.4 Ventajas y desventajas del enfoque de seguridad')
    d.pros_cons(['La seguridad no depende de la app: se aplica en el servidor', 'Sin servidor propio que proteger', 'Historial completo de cambios administrativos'],
                ['Las reglas son un lenguaje más a mantener', 'Sin autenticación de dos factores en esta versión', 'Respaldos manuales en el plan gratuito'])

    d.h1('18. Vistas: qué cambia entre móvil y web')
    d.p('La app es la misma, pero se adapta al dispositivo y a lo que la persona necesita hacer ahí.')
    d.table(['Aspecto', 'Móvil (Android / iPhone)', 'Web (computadora)'], [
        ['Para qué se usa', 'Reservar sobre la marcha, consultar la reserva, abrir la habitación, recepción en el lobby', 'Planear con calma y administrar el hotel'],
        ['Navegación', 'Barra inferior con 5 pestañas al alcance del pulgar', 'Riel lateral con todas las pestañas del rol'],
        ['Distribución', 'Una columna; el presupuesto se pliega en "Desglose"', 'Varias columnas; presupuesto siempre visible al lado'],
        ['Funciones exclusivas', 'Llave digital', 'Panel de administración, catálogo y superusuario'],
        ['Recepción (STAFF)', 'Sí: listas del día en el móvil del turno', 'Sí'],
        ['Tablas e indicadores', 'No (pantalla pequeña)', 'Sí: reservas con filtros e ingresos por habitación'],
        ['Ubicación', 'Permiso del sistema Android/iOS', 'Permiso del navegador'],
        ['Instalación', 'APK (o tienda en el futuro)', 'Ninguna: se abre con un enlace'],
        ['Actualizaciones', 'Hay que instalar la nueva versión', 'Inmediatas al recargar'],
        ['Sin conexión', 'Conserva reservas y preferencias locales', 'También, mientras no se borre el navegador'],
    ], [3.4, 6.3, 6.3], 'Móvil frente a web', 8.5)
    d.shots([('movil_reserva_paso1.jpg', 'Móvil: una columna'), ('movil_mis_reservas.jpg', 'Móvil: barra inferior')], 4.6)
    d.shot('web_05_reserva_presupuesto.jpg', 'Web: presupuesto fijo al lado y riel lateral.', 14)
    d.h2('18.1 Ventajas y desventajas de la vista móvil')
    d.pros_cons(['Siempre a mano y rápida', 'Llave digital y notificaciones posibles', 'Funciona con mala conexión'],
                ['Pantalla pequeña: no caben tablas ni paneles', 'Requiere instalar y actualizar', 'Para iPhone hace falta la App Store'])
    d.h2('18.2 Ventajas y desventajas de la vista web')
    d.pros_cons(['Sin instalación; un enlace basta', 'Pantalla grande para administrar', 'Se actualiza al instante'],
                ['Menos práctica de pie o de viaje', 'Sin llave digital', 'Primera carga más pesada (WebAssembly)'])
    d.tap(19, ['Especifica pantallas, navegación, validaciones y retroalimentación (RF-01…RF-18).',
               'Especifica qué operaciones son inmediatas y cuáles asíncronas (red, sincronización, animaciones).',
               'Especifica las operaciones de consulta, alta y actualización con reglas en el servidor.',
               'Define actores, plataformas y la norma "móvil útil / web completa".'])
    return d.save()


# ======================================================================================
# E2. LIBRERÍAS Y COMPONENTES
# ======================================================================================
LIBS = [
    # nombre, versión, propósito, requisitos, instalación, configuración, dependencias, uso, entradas/salidas, ejemplo, limitaciones
    dict(n='Compose Multiplatform (runtime, foundation, ui, material3)', v='1.11.1 · Material3 1.11.0-alpha07',
         prop='Construir toda la interfaz declarativa una sola vez para Android, iOS y web.',
         req='Kotlin 2.4, plugin org.jetbrains.compose y compose-compiler; navegador con WasmGC (Chrome 119+, Firefox 120+, Safari 18.2+).',
         inst='plugins { alias(libs.plugins.composeMultiplatform); alias(libs.plugins.composeCompiler) }\ncommonMain.dependencies { implementation(libs.compose.material3) }',
         conf='Tema propio LumbreTheme (colores, tipografía Playfair/Inter, formas). Opt-in de APIs experimentales en el build.',
         dep='Skiko (motor gráfico en iOS/web), kotlinx-coroutines.',
         uso='Funciones @Composable que describen la UI según el estado; el estado se lee de StateFlow con collectAsState().',
         io='Entrada: estado (StateFlow, remember). Salida: árbol de UI renderizado; eventos vía lambdas (onClick, onValueChange).',
         ej='@Composable fun Saludo(nombre: String) {\n  Text("Hola, $nombre", style = MaterialTheme.typography.titleLarge)\n}',
         lim='Material3 en alfa; en web el primer arranque descarga ~8 MB; no corre en Node.js (Skiko), por eso las pruebas van en JVM.'),
    dict(n='Navigation Compose (JetBrains)', v='2.9.2',
         prop='Navegación con rutas tipadas, pila atrás y transiciones compartidas.',
         req='Compose Multiplatform y kotlinx-serialization.', inst='implementation(libs.navigation.compose)',
         conf='Rutas @Serializable (HomeRoute, BookingRoute(room, promo)…) y NavHost con animaciones.',
         dep='lifecycle, serialization.', uso='navController.navigate(BookingRoute(promo = "LUMBRE10"))',
         io='Entrada: objeto de ruta con argumentos. Salida: pantalla destino con argumentos tipados (toRoute()).',
         ej='composable<BookingRoute> { e -> BookingScreen(e.toRoute<BookingRoute>().promo) }',
         lim='En web no sincroniza la URL del navegador automáticamente.'),
    dict(n='Ktor Client', v='3.5.1 (motores okhttp, darwin, js)',
         prop='Cliente HTTP multiplataforma para las API REST de Firebase y de geolocalización.',
         req='Un motor por plataforma.', inst='commonMain: ktor-client-core, content-negotiation, serialization-kotlinx-json\nandroidMain: ktor-client-okhttp · iosMain: ktor-client-darwin · wasmJsMain: ktor-client-js',
         conf='HttpClient compartido con ContentNegotiation(Json { ignoreUnknownKeys = true }).', dep='kotlinx-coroutines, kotlinx-serialization.',
         uso='Funciones suspend que hacen post/get/patch y devuelven JsonObject.', io='Entrada: URL, cuerpo JSON, cabeceras (Bearer token). Salida: respuesta JSON o FirebaseException(code, status).',
         ej='val r = http.post(url) { contentType(ContentType.Application.Json); setBody(body) }',
         lim='En web hereda las restricciones CORS del navegador.'),
    dict(n='Firebase Authentication (REST Identity Toolkit)', v='API v1 · plan Spark',
         prop='Registro, inicio de sesión, verificación de correo, restablecimiento y cambio de contraseña.',
         req='Proyecto Firebase con proveedor correo/contraseña activo y clave de API web.', inst='Sin SDK: se consume por REST con Ktor (FirebaseAuthApi.kt).',
         conf='FirebaseConfig.API_KEY y PROJECT_ID; dominios autorizados en la consola.', dep='Ktor.',
         uso='FirebaseAuthApi.signIn(email, pass) → Session(idToken, refreshToken, uid).',
         io='Entrada: correo, contraseña. Salida: idToken (1 h), refreshToken, localId; errores EMAIL_EXISTS, INVALID_LOGIN_CREDENTIALS, TOO_MANY_ATTEMPTS_TRY_LATER.',
         ej='val s = FirebaseAuthApi.signUp(email, password)\nFirebaseAuthApi.sendEmailVerification(s.idToken)',
         lim='La clave de API es pública por diseño (la seguridad está en las reglas); sin inicio de sesión social en esta versión.'),
    dict(n='Cloud Firestore (REST)', v='API v1 · base (default), nam5',
         prop='Base de datos en la nube de usuarios, catálogo, promociones, reservas, parámetros y auditoría.',
         req='Autenticación previa para colecciones privadas.', inst='Sin SDK: FirestoreApi(token) con códec propio (FirestoreCodec).',
         conf='Reglas en app/firebase/firestore.rules publicadas en la consola.', dep='Ktor, Firebase Auth.',
         uso='FirestoreApi(token).set("reservations", ref, fields) · whereEquals("reservations", "uid", uid)',
         io='Entrada: colección, id, Map<String, Any?>. Salida: FsDoc(id, fields) o lista; 403 si la regla lo impide.',
         ej='api.update("users", uid, mapOf("lang" to "EN"))  // PATCH con updateMask',
         lim='Sin escucha en tiempo real por REST (se refresca); 50 000 lecturas/día en el plan gratuito.'),
    dict(n='kotlinx-datetime', v='0.7.1', prop='Fechas sin hora (LocalDate), sumas de días/meses y día de la semana para recargos.',
         req='—', inst='implementation(libs.kotlinx.datetime)', conf='Zona horaria del sistema para "hoy".', dep='—',
         uso='checkIn.daysUntil(checkOut); date.plus(18, DateTimeUnit.MONTH)', io='Entrada: año, mes, día. Salida: LocalDate y diferencias.',
         ej='val noches = LocalDate(2026,12,1).daysUntil(LocalDate(2026,12,4)) // 3', lim='Formateo localizado propio (Format.kt).'),
    dict(n='kotlinx-serialization-json', v='1.9.0', prop='Serializar reservas y preferencias locales y rutas de navegación.',
         req='Plugin kotlin("plugin.serialization").', inst='implementation(libs.kotlinx.serialization.json)', conf='Json { ignoreUnknownKeys = true }', dep='—',
         uso='Json.encodeToString(lista)', io='Entrada: objeto @Serializable. Salida: texto JSON y viceversa.',
         ej='@Serializable data class Prefs(val lang: Lang, val currency: Currency)', lim='Requiere anotar cada clase.'),
    dict(n='multiplatform-settings (no-arg)', v='1.3.0', prop='Almacenamiento clave-valor local (SharedPreferences, NSUserDefaults, localStorage).',
         req='—', inst='implementation(libs.multiplatform.settings)', conf='Settings() sin argumentos.', dep='—',
         uso='settings.putString("prefs", json)', io='Entrada: clave y valor. Salida: valor guardado o predeterminado.',
         ej='val token = settings.getStringOrNull("refresh")', lim='No cifrado: solo se guardan datos no sensibles y el token de renovación.'),
    dict(n='BigDataCloud reverse-geocode-client', v='API gratuita sin clave', prop='Convertir coordenadas aproximadas en código de país.',
         req='Conexión y consentimiento de ubicación.', inst='Llamada GET con Ktor (Location.kt).', conf='Coordenadas redondeadas a 1 decimal.', dep='Ktor.',
         uso='countryFromCoordinates(19.7, -101.2) → "MX"', io='Entrada: lat, lon. Salida: código ISO-3166 o null (se usa roughCountry sin conexión).',
         ej='val pais = countryFromCoordinates(lat, lon) ?: roughCountry(lat, lon)', lim='Precisión de país; tabla de respaldo aproximada.'),
]

OWN = [
    ['Pricing.quote', 'room, checkIn, checkOut, adults, children, extras, promoPercent, params', 'Quote? (líneas, noches, total) o null si fechas inválidas', 'Cálculo del presupuesto.'],
    ['Validation.email / name / phone', 'String', 'K? (clave de error) o null si es válido', 'Validación de formularios.'],
    ['Validation.dates', 'checkIn, checkOut, today, params', 'K? (E_PAST, E_ORDER, E_MAXSTAY, E_FAR)', 'Reglas de fechas.'],
    ['Validation.password / passwordStrength', 'value, minLength, email', 'K? / Int 0..4', 'Política de contraseñas.'],
    ['Format.money', 'eur, currency, lang', 'String ("MX$12,415")', 'Conversión y formato de moneda.'],
    ['HotelRepository', 'acciones (login, book, setStatus…)', 'StateFlow (prefs, rooms, reservations, account, role…)', 'Fuente única de verdad.'],
    ['Capabilities', 'plataforma, rol', 'Boolean por función', 'Norma móvil/web.'],
    ['rememberLocationRequester', 'onResult(LocationResult)', 'función que pide ubicación', 'expect/actual por plataforma.'],
    ['LumbreButton', 'text, icon, style, enabled, onClick', 'Botón con rebote y estilos Primary/Sun/Ghost', 'UI.'],
    ['Lumi / LumiSays', 'mood, trigger, text', 'Mascota animada con globo', 'Guía y feedback.'],
    ['Stepper', 'label, hint, value, range, onChange', 'Selector − valor +', 'Huéspedes.'],
    ['PhotoCard, StatusChip, AnimatedMoney', 'datos', 'Tarjeta con foto, chip de estado, cifra animada', 'UI.'],
    ['ConfettiBurst, WavesEdge, glass, FloatingIcon', 'key / color / forma', 'Efectos vacacionales', 'UI.'],
    ['ConsentBanner, PrivacyScreen', 'estado de consentimiento', 'Aviso y pantalla de cookies', 'Privacidad.'],
    ['GuardNotice', 'mensaje', 'Aviso de acceso restringido', 'Seguridad en UI.'],
]


PCL = {'Compose Multiplatform': (['Una sola interfaz para 3 plataformas', 'Animaciones potentes', 'Comunidad grande (JetBrains/Google)'], ['Material 3 aún en alfa', 'Web pesa más en la primera carga', 'Pruebas de UI no corren en Node']), 'Navigation Compose': (['Rutas con tipos: menos errores', 'Transiciones animadas'], ['No sincroniza la URL del navegador']), 'Ktor Client': (['Mismo código de red en todas las plataformas', 'Asíncrono, no bloquea'], ['Hay que configurar un motor por plataforma']), 'Firebase Authentication': (['Cuentas seguras sin servidor propio', 'Verificación y recuperación incluidas'], ['Sin SDK oficial para Wasm: se usó REST', 'Dependencia de Google']), 'Cloud Firestore': (['Reglas por usuario en el servidor', 'Gratis para este volumen'], ['Sin JOIN', 'Sin tiempo real por REST']), 'kotlinx-datetime': (['Fechas correctas en todas las plataformas'], ['Formato local hecho a mano']), 'kotlinx-serialization-json': (['Rápida y sin reflexión', 'Funciona en Wasm'], ['Hay que anotar cada clase']), 'multiplatform-settings': (['Cero configuración', 'Usa el almacenamiento nativo'], ['No cifra los datos']), 'BigDataCloud': (['Gratis y sin clave', 'Precisión de país suficiente'], ['Servicio externo: puede cambiar sus condiciones'])}


def e2():
    d = Doc('U2_Librerias/U2_E2_Librerias_y_Componentes.docx', U, 'Entregable 2', 'Librerías y componentes',
            'Documentación de cada librería y componente: propósito, requisitos, instalación, configuración, uso, E/S, ejemplos y limitaciones')
    d.toc(['Mapa de dependencias', 'Entorno de desarrollo', 'Fichas de librerías externas', 'Componentes propios del equipo',
           'Ejemplo integrado', 'Guía de instalación del proyecto completo', 'Compatibilidad de versiones', 'Licencias', 'Componentes síncronos y asíncronos', 'Criterios TAP'])
    d.h1('1. Mapa de dependencias')
    d.diagram('09_dependencias_externas.png', 'Librerías y servicios externos usados por cada módulo.', 15.5)
    d.h1('2. Entorno de desarrollo')
    d.table(['Herramienta', 'Versión', 'Uso'], [
        ['Android Studio (con JBR 21)', '2026.x', 'IDE y JDK para Gradle.'],
        ['Kotlin', '2.4.10', 'Lenguaje.'], ['Gradle', '9.4.1', 'Construcción.'], ['Android Gradle Plugin', '9.2.1', 'Plugin com.android.kotlin.multiplatform.library.'],
        ['Android SDK', 'compileSdk/targetSdk 37, minSdk 26', 'APK.'], ['Xcode (macOS)', '16+', 'Compilar iOS (opcional).'],
        ['Node / Yarn (gestionado por Gradle)', '—', 'Empaquetado web.'], ['GitHub Actions + Pages', '—', 'CI y publicación.'],
    ], [5.5, 4.5, 6], 'Entorno')
    d.h1('3. Fichas de librerías externas')
    for i, L in enumerate(LIBS, 1):
        d.h2(f'3.{i} {L["n"]}')
        d.table(['Aspecto', 'Detalle'], [
            ['Versión', L['v']], ['Propósito', L['prop']], ['Requisitos', L['req']], ['Configuración', L['conf']],
            ['Dependencias', L['dep']], ['Uso', L['uso']], ['Parámetros de entrada / salida', L['io']], ['Limitaciones', L['lim']],
        ], [4, 12], None, 9)
        d.code(L['inst'], 'Instalación (Gradle, catálogo libs.versions.toml).')
        d.code(L['ej'], 'Ejemplo de uso.')
        for k, (pros, cons) in PCL.items():
            if L['n'].startswith(k):
                d.pros_cons(pros, cons, f'Ventajas y desventajas de {k}')
                break
    d.h1('4. Componentes propios del equipo')
    d.p('Además de las librerías externas, el equipo construyó componentes reutilizables en el módulo shared. Todos son '
        'multiplataforma y están cubiertos por pruebas o usados en varias pantallas.')
    d.table(['Componente', 'Entradas', 'Salidas', 'Propósito'], OWN, [4, 4.6, 4.6, 2.8], 'Componentes propios', 8.5)
    d.code('''val q = Pricing.quote(
    room = RoomConfig(RoomId.DELUXE, nightlyEur = 190, capacity = 3),
    checkIn = LocalDate(2026, 12, 1), checkOut = LocalDate(2026, 12, 4),
    adults = 2, children = 0, extras = emptySet(), promoPercent = 0, params = Params())
// q.nights == 3, q.totalEur == 627.0  (570 de noches + 57 de impuestos)''', 'Ejemplo de Pricing.quote, verificado por PricingTest.')
    d.h1('5. Ejemplo integrado')
    d.p('Flujo real de "iniciar sesión y ver mis reservas" usando varias librerías a la vez:')
    d.diagram('07_secuencia_login.png', 'Secuencia de inicio de sesión: Compose → HotelRepository → Ktor → Firebase.', 15.5)
    d.h1('6. Guía de instalación del proyecto completo')
    d.bullets([
        f'git clone {REPO}',
        'Abrir la carpeta app/ en Android Studio y esperar la sincronización de Gradle.',
        'Android: ./gradlew :androidApp:assembleDebug → app/androidApp/build/outputs/apk/debug/.',
        'Web: ./gradlew :webApp:wasmJsBrowserDevelopmentRun (o wasmJsBrowserDistribution para producción).',
        'iOS: abrir iosApp/iosApp.xcodeproj en Xcode (macOS) y ejecutar.',
        'Pruebas: ./gradlew :shared:testAndroidHostTest.',
        'Firebase propio (opcional): cambiar API_KEY y PROJECT_ID en FirebaseConfig.kt y publicar firestore.rules.',
    ], numbered=True)
    d.h1('7. Compatibilidad de versiones')
    d.note('Kotlin 2.4.10 + Compose Multiplatform 1.11.1 + AGP 9.2.1 exigen el nuevo plugin '
           'com.android.kotlin.multiplatform.library (bloque androidLibrary {}). Al añadir Ktor hubo que regenerar '
           'kotlin-js-store/wasm/yarn.lock con kotlinWasmUpgradeYarnLock.', 'Lección aprendida')
    d.h1('8. Licencias')
    d.table(['Librería / recurso', 'Licencia'], [
        ['Compose Multiplatform, Navigation, kotlinx-*', 'Apache 2.0'], ['Ktor', 'Apache 2.0'], ['multiplatform-settings', 'Apache 2.0'],
        ['Firebase (servicio)', 'Términos de Google Firebase, plan Spark gratuito'], ['BigDataCloud client API', 'Uso gratuito con atribución'],
        ['Fotografías', 'Licencia Unsplash'], ['Fuentes Playfair Display e Inter', 'SIL Open Font License'], ['PlantUML (diagramas)', 'MIT'],
    ], [8, 8], 'Licencias')
    d.h1('9. Componentes síncronos y asíncronos')
    d.table(['Componente / librería', 'Tipo', 'Uso en el proyecto'], [
        ['Pricing, Validation, Format', 'Síncrono (funciones puras)', 'Cálculo y validación instantáneos en el hilo de la UI'],
        ['MutableStateFlow / StateFlow', 'Asíncrono reactivo', 'Estado observable; collectAsState() recompone la UI'],
        ['MutableSharedFlow (events)', 'Asíncrono (eventos)', 'Mensajes de error/éxito hacia el Snackbar'],
        ['combine()', 'Asíncrono reactivo', 'El rol se deriva de cuenta + modo demo'],
        ['CoroutineScope(SupervisorJob + Dispatchers.Default)', 'Concurrencia estructurada', 'Escrituras remotas independientes; un fallo no cancela las demás'],
        ['suspend fun (34)', 'Asíncrono', 'Llamadas a Firebase y geolocalización sin bloquear'],
        ['Ktor HttpClient', 'E/S no bloqueante', 'Motores OkHttp, Darwin y JS'],
        ['LaunchedEffect / rememberCoroutineScope', 'Asíncrono ligado a la UI', 'Animaciones, temporizadores (delay) y acciones de botones'],
    ], [5.5, 3.5, 7], 'Clasificación síncrono/asíncrono', 9)
    d.diagram('14_concurrencia.png', 'Secuencia de una reserva: parte síncrona y parte asíncrona.', 15)
    d.diagram('16_clases_dominio.png', 'Clases de los componentes propios.', 16)
    d.tap(10, ['Documenta los componentes visuales reutilizables (LumbreButton, Stepper, Lumi…).',
               'Clasifica cada librería y componente como síncrono o asíncrono y explica la concurrencia.',
               'Documenta Ktor, Firebase Auth y Firestore como capa de acceso a datos.',
               'Muestra que las librerías elegidas son multiplataforma para la app móvil.'])
    return d.save()


# ======================================================================================
# E3. APLICACIÓN DEL EQUIPO
# ======================================================================================
def e3():
    d = Doc('U2_Librerias/U2_E3_Aplicacion_del_Equipo.docx', U, 'Entregable 3', 'Aplicación desarrollada por el equipo',
            'Lumbre Hotel & Spa: descripción, módulos, pantallas, pruebas, publicación y manual de uso')
    d.toc(['Descripción', 'Tecnologías', 'Estructura del proyecto', 'Pantallas y funciones', 'Diferencias móvil y web',
           'Cuentas, roles y paneles', 'Pruebas', 'Integración continua y publicación', 'Manual rápido de uso', 'Métricas del proyecto', 'Arquitectura y documentación técnica', 'Vistas móvil y web', 'Criterios TAP'])
    d.h1('1. Descripción')
    d.p('Aplicación de reservas para un hotel boutique frente al mar, con estética vacacional (fotos de playa, piscinas, '
        'gastronomía y excursiones; paleta turquesa, arena y sol) y una mascota guía. Funciona en Android, iOS y web desde un '
        'mismo código y guarda cuentas y reservas en Firebase, de modo que lo que haces en el móvil aparece en la web.')
    d.h1('2. Tecnologías')
    d.table(['Capa', 'Tecnología'], [
        ['Lenguaje', 'Kotlin 2.4 (Multiplatform)'], ['Interfaz', 'Compose Multiplatform 1.11 + Material 3'],
        ['Navegación', 'Navigation Compose con rutas tipadas'], ['Red', 'Ktor 3.5'], ['Nube', 'Firebase Authentication + Cloud Firestore (gratis)'],
        ['Almacenamiento local', 'multiplatform-settings'], ['Web', 'Kotlin/Wasm en GitHub Pages'], ['CI/CD', 'GitHub Actions'],
    ], [5, 11], 'Tecnologías')
    d.h1('3. Estructura del proyecto')
    d.code('''app/
├─ shared/src/commonMain/kotlin/com/lumbre/hotel/
│  ├─ App.kt                 navegación, pestañas por rol, avisos
│  ├─ data/                  Models, HotelRepository, firebase/ (Auth, Firestore, Mappers)
│  ├─ domain/                Pricing, Validation, Format
│  ├─ i18n/                  Strings (ES, EN, PT, FR)
│  ├─ platform/              Platform/Capabilities, Location (expect)
│  └─ ui/                    theme, components, navigation, screens (14 pantallas)
├─ shared/src/{androidMain,iosMain,wasmJsMain}/   implementaciones actual
├─ shared/src/commonTest/   PricingTest, ValidationTest
├─ androidApp/  iosApp/  webApp/                  puntos de entrada
└─ firebase/firestore.rules''')
    d.h1('4. Pantallas y funciones')
    shots = [
        ('movil_01_inicio.jpg', 'Inicio (móvil): buscador de fechas y huéspedes sobre la foto del hotel.', 7),
        ('web_03_habitaciones.jpg', 'Habitaciones (web) con precio en la moneda detectada (MXN).', 15),
        ('web_04_ofertas.jpg', 'Ofertas: código LUMBRE10 y descuentos automáticos.', 15),
        ('web_05_reserva_presupuesto.jpg', 'Reserva paso 1 con presupuesto en vivo y código aplicado.', 15),
        ('web_06_reserva_datos.jpg', 'Reserva paso 3: datos del huésped.', 15),
        ('web_08_iniciar_sesion.jpg', 'Perfil: iniciar sesión.', 15),
        ('web_09_crear_cuenta.jpg', 'Crear cuenta con medidor de fuerza de contraseña.', 15),
        ('web_02_privacidad.jpg', 'Cookies y privacidad.', 15),
    ]
    for f, c, w in shots:
        d.shot(f, c, w)
    d.h1('5. Diferencias móvil y web')
    d.p('La app es la misma, pero la función Capabilities activa o desactiva secciones:')
    d.bullets([
        'Móvil: barra inferior con Inicio, Habitaciones, Ofertas, Reservas y Perfil; llave digital; recepción para personal.',
        'Web: riel lateral con todas las pestañas permitidas por el rol, incluidos Administración y Superusuario.',
        'En el perfil, la sección "Qué puedes hacer aquí" explica qué está disponible en la plataforma actual.',
    ])
    d.shot('movil_02_preferencias_capacidades.jpg', 'Preferencias y "Qué puedes hacer aquí".', 7)
    d.h1('6. Cuentas, roles y paneles')
    d.table(['Panel', 'Rol mínimo', 'Plataforma', 'Contenido'], [
        ['Recepción', 'STAFF', 'Móvil y web', 'Llegadas, en el hotel, salidas; registrar llegada.'],
        ['Administración', 'STAFF', 'Web', 'Reservas con filtros e indicadores.'],
        ['Catálogo', 'ADMIN', 'Web', 'Precios, disponibilidad y promociones.'],
        ['Superusuario', 'SUPERADMIN', 'Web', 'Usuarios (rol y bloqueo), Parámetros, Auditoría, Seguridad.'],
    ], [3, 2.8, 3, 7.2], 'Paneles')
    d.p('La cuenta del propietario del proyecto recibe el rol SUPERADMIN directamente en Firestore (el único camino '
        'permitido para el primer superusuario); después, ese superusuario puede asignar roles desde su panel.')
    d.h1('7. Pruebas')
    d.table(['Suite', 'Pruebas', 'Qué cubre', 'Resultado'], [
        ['PricingTest', '6', 'Noches entre semana, recargo de fin de semana, larga estancia + promo, extras por unidad, parámetros, fechas inválidas.', '6/6 ✔'],
        ['ValidationTest', '8', 'Correos y sugerencias, nombres y teléfonos, contraseñas, fechas, moneda, detección de idioma/moneda y país, roles, traducciones, códec Firestore.', '8/8 ✔'],
    ], [3, 1.6, 9, 2.4], 'Pruebas unitarias (./gradlew :shared:testAndroidHostTest)')
    d.p('Pruebas manuales: flujo de reserva completo, validaciones (captura en E1), cookies y ubicación, cambio de idioma y '
        'moneda, tema oscuro, diseño en 375 px y 1280 px, instalación del APK en emulador Android.')
    d.h1('8. Integración continua y publicación')
    d.p('Cada push a main ejecuta GitHub Actions: compila la web Wasm y el APK y publica en GitHub Pages la página del hotel '
        f'({WEB}), la app web ({APPWEB}) y el APK ({APK}).')
    d.h1('9. Manual rápido de uso')
    d.bullets(['Abre la app y elige tus cookies (con "Aceptar todo" detecta idioma y moneda por tu ubicación).',
               'En Inicio elige fechas y huéspedes y pulsa "Ver precios".', 'Elige habitación y extras; revisa el presupuesto.',
               'Escribe tus datos, acepta y confirma: recibirás la referencia LMB-XXXXXX.',
               'Crea una cuenta en Perfil para ver tus reservas en cualquier dispositivo.'], numbered=True)
    d.h1('10. Métricas del proyecto')
    d.table(['Métrica', 'Valor'], [['Líneas de Kotlin en shared', '≈ 7 300'], ['Pantallas', '14'], ['Claves de texto traducidas', '> 400 × 4 idiomas'],
                                   ['Plataformas', 'Android, iOS, web'], ['Pruebas unitarias', '14'], ['Costo de operación', '0 €']], [8, 8], 'Métricas')
    d.h1('11. Arquitectura y documentación técnica')
    d.diagram('19_arquitectura_modulos.png', 'Arquitectura por módulos del repositorio (basada en gitdiagram.com).', 16)
    d.diagram('08_despliegue.png', 'Despliegue: GitHub Pages, APK y Firebase.', 15)
    d.h2('11.1 Paneles por rol (capturas reales)')
    for f, c in (('escritorio_admin_panel.jpg', 'Administración: indicadores e ingresos por habitación.'),
                 ('escritorio_admin_catalogo.jpg', 'Catálogo: precio por noche y disponibilidad.'),
                 ('escritorio_recepcion.jpg', 'Recepción del día.'),
                 ('escritorio_super_parametros.jpg', 'Superusuario: parámetros.'),
                 ('escritorio_super_seguridad.jpg', 'Superusuario: estado de seguridad.')):
        d.shot(f, c, 15)
    d.h2('11.2 Flujo móvil completo')
    d.shots([('movil_reserva_paso1.jpg', 'Fechas'), ('movil_reserva_extras.jpg', 'Habitación y extras'), ('movil_reserva_paso3.jpg', 'Datos')], 4.6)
    d.shots([('movil_confirmacion.jpg', 'Confirmación'), ('movil_mis_reservas.jpg', 'Mis reservas'), ('movil_cancelar_dialogo.jpg', 'Cancelar')], 4.6, 'Reserva completa en el teléfono.')
    d.h2('11.3 Reglas de seguridad de Firestore (archivo completo)')
    d.code(open(os.path.join(ROOT, 'app', 'firebase', 'firestore.rules'), encoding='utf-8').read(), 'app/firebase/firestore.rules')
    d.h2('11.4 Integración y despliegue continuo')
    d.code(open(os.path.join(ROOT, '.github', 'workflows', 'pages.yml'), encoding='utf-8').read(), '.github/workflows/pages.yml')
    d.h1('12. Vistas móvil y web en la aplicación')
    d.p('Resumen de lo que cambia entre plataformas (detalle completo y ventajas/desventajas en U2_E1 §18).')
    d.shots([('movil_ofertas.jpg', 'Ofertas en móvil'), ('movil_detalle_habitacion.jpg', 'Detalle en móvil')], 4.6)
    d.shot('web_04_ofertas.jpg', 'Ofertas en web.', 13)
    d.pros_cons(['Un solo código: lo que se corrige en uno se corrige en todos', 'Cada plataforma muestra lo que tiene sentido ahí'],
                ['Hay que probar en varios tamaños de pantalla', 'Algunas funciones no existen en todas las plataformas'],
                'Una app adaptable: ventajas y desventajas')
    d.tap(13, ['Muestra todas las pantallas web y móvil y los paneles por rol.',
               'Describe la sincronización en segundo plano y la actualización optimista.',
               'Incluye las reglas de seguridad completas que protegen el acceso a datos.',
               'Demuestra la app funcionando en el teléfono con las funciones útiles.'])
    return d.save()


# ======================================================================================
# E4. APLICACIÓN CON COMPONENTES EXTERNOS + FEEDBACK
# ======================================================================================
def e4():
    d = Doc('U2_Librerias/U2_E4_Componentes_Externos_y_Feedback.docx', U, 'Entregable 4', 'Aplicación con componentes externos y retroalimentación',
            'Integración de componentes de la web y repositorios públicos, vistos como oportunidad, y feedback sobre ellos')
    d.toc(['Planteamiento', 'Componentes externos integrados', 'Proceso de integración', 'Problemas encontrados y oportunidades',
           'Retroalimentación para los autores de los componentes', 'Retroalimentación recibida sobre nuestra aplicación', 'Mejoras aplicadas', 'Conclusión', 'Ventajas y desventajas', 'Criterios TAP'])
    d.h1('1. Planteamiento')
    d.p('La actividad propone integrar componentes desarrollados por otro equipo. En este proyecto no se usaron componentes '
        'de otro equipo del grupo; en su lugar se integraron componentes publicados en la web y en repositorios abiertos '
        '(JetBrains, Google, Ktor, comunidad). Funcionalmente es la misma situación: código que no escribimos, con su propia '
        'documentación, decisiones y limitaciones. Lejos de ser un problema, fue una oportunidad para aprender a evaluar, '
        'adaptar y dar retroalimentación a componentes ajenos, como ocurre en proyectos reales.')
    d.h1('2. Componentes externos integrados')
    d.table(['Componente', 'Origen', 'Para qué lo usamos', 'Esfuerzo'], [
        ['Plantilla KMP (Android + iOS + Web)', 'Asistente kmp.jetbrains.com', 'Esqueleto del proyecto multiplataforma.', 'Bajo'],
        ['Compose Multiplatform + Material 3', 'github.com/JetBrains/compose-multiplatform', 'Toda la UI.', 'Medio'],
        ['Navigation Compose', 'JetBrains (fork de AndroidX)', 'Rutas tipadas y transiciones compartidas.', 'Medio'],
        ['Ktor Client', 'github.com/ktorio/ktor', 'Peticiones HTTP a Firebase y geolocalización.', 'Bajo'],
        ['Firebase Auth + Firestore (REST)', 'Google', 'Cuentas, roles y datos en la nube.', 'Alto'],
        ['multiplatform-settings', 'github.com/russhwolf', 'Almacenamiento local.', 'Bajo'],
        ['BigDataCloud reverse geocode', 'bigdatacloud.com', 'País a partir de coordenadas.', 'Bajo'],
        ['Fotografías', 'Unsplash', 'Ambiente vacacional.', 'Bajo'],
        ['Tipografías Playfair Display e Inter', 'Google Fonts', 'Identidad visual.', 'Bajo'],
        ['PlantUML', 'plantuml.com (MIT)', 'Generar los diagramas de la documentación.', 'Bajo'],
    ], [4.2, 4.6, 5.2, 2], 'Componentes externos')
    d.diagram('09_dependencias_externas.png', 'Dónde se integra cada componente externo.', 15)
    d.h1('3. Proceso de integración')
    d.bullets([
        ('Selección', 'se comparó cada opción por licencia, soporte multiplataforma, mantenimiento (último release) y costo.'),
        ('Prueba aislada', 'cada componente se probó primero en un ejemplo mínimo (p. ej. una llamada signUp con Ktor).'),
        ('Envoltura', 'se encapsuló detrás de una interfaz propia (FirebaseAuthApi, FirestoreApi, rememberLocationRequester) para poder sustituirlo.'),
        ('Integración', 'se conectó al repositorio HotelRepository y a las pantallas.'),
        ('Verificación', 'pruebas unitarias, compilación en las tres plataformas y prueba manual.'),
    ], numbered=True)
    d.h1('4. Problemas encontrados y oportunidades')
    d.table(['Problema real', 'Causa', 'Solución', 'Oportunidad / aprendizaje'], [
        ['No existe SDK oficial de Firebase para Kotlin/Wasm', 'Firebase publica SDK para Android, iOS y JS, no para KMP-Wasm.', 'Consumir las API REST con Ktor y escribir un códec Firestore propio.', 'Entender a fondo el protocolo y no depender de un SDK; el mismo código sirve en las 3 plataformas.'],
        ['El build web falló tras añadir Ktor', 'yarn.lock de Kotlin/Wasm bloqueado.', 'Tarea kotlinWasmUpgradeYarnLock.', 'Conocer la protección de dependencias npm de Gradle.'],
        ['Las pruebas no corren en Node.js', 'Skiko (motor de Compose) necesita navegador.', 'Ejecutar commonTest en la JVM con withHostTest {}.', 'Separar lógica de dominio de la UI facilita probarla.'],
        ['AGP 9 cambió el plugin Android de KMP', 'Nuevo com.android.kotlin.multiplatform.library.', 'Migrar al bloque androidLibrary {}.', 'Leer notas de versión antes de actualizar.'],
        ['Error "Activity class does not exist" en Android', 'Nombre relativo de la actividad en el manifiesto.', 'Nombre completo com.lumbre.hotel.MainActivity.', 'Revisar el namespace de cada módulo.'],
        ['Geolocalización distinta por plataforma', 'API del navegador vs. LocationManager de Android vs. CoreLocation.', 'expect/actual con un resultado común (LocationResult).', 'Diseñar interfaces comunes sobre APIs nativas.'],
        ['Diagramas con caracteres especiales rotos', 'PlantUML interpreta ">" dentro de estereotipos.', 'Reescribir restricciones con palabras.', 'Validar cada salida generada.'],
    ], [3.6, 3.6, 4.2, 4.6], 'Problemas y oportunidades', 8.5)
    d.h1('5. Retroalimentación para los autores de los componentes')
    d.p('Como consumidores externos, documentamos lo que mejoraría cada componente (formato de issue constructivo):')
    d.table(['Componente', 'Lo que funcionó bien', 'Sugerencia de mejora'], [
        ['Compose Multiplatform', 'Misma API en las 3 plataformas; animaciones y SharedTransition muy potentes.', 'Permitir pruebas de UI en Node; reducir el tamaño inicial de la web.'],
        ['Firebase REST', 'Documentación clara de errores; reglas muy expresivas.', 'Publicar un SDK oficial para Kotlin Multiplatform; ejemplos REST de Firestore con updateMask.'],
        ['Ktor', 'Un cliente común con motor por plataforma; muy fácil de configurar.', 'Ejemplos de manejo de errores HTTP tipados.'],
        ['Navigation Compose', 'Rutas tipadas con serialización.', 'Sincronizar la URL del navegador en web.'],
        ['multiplatform-settings', 'Cero configuración.', 'Variante cifrada multiplataforma.'],
        ['BigDataCloud', 'Gratis y sin clave.', 'Indicar límites de uso en la respuesta.'],
    ], [3.5, 6, 6.5], 'Feedback hacia los componentes')
    d.h1('6. Retroalimentación recibida sobre nuestra aplicación')
    d.p('La retroalimentación real provino de las revisiones del responsable del producto durante el desarrollo '
        '(observaciones sobre cada versión publicada) y de las pruebas propias del equipo:')
    d.table(['Observación recibida', 'Versión', 'Respuesta del equipo'], [
        ['"Esa paleta es muy oscura, añade un tema blanco."', 'App v1', 'Tema claro por defecto, oscuro opcional y modo sistema.'],
        ['"Es un hotel: imágenes, colores y animaciones de vacaciones."', 'App v1', 'Fotos de playa, piscinas, comida y excursiones; olas, efecto cristal e iconos flotantes.'],
        ['"Que todos los botones funcionen."', 'App v1', 'Revisión de cada acción; botones sin destino eliminados o conectados.'],
        ['"Cosas que solo se puedan hacer en web y no en móvil."', 'App v1', 'Capabilities por plataforma y rol.'],
        ['"Cuentas en Firebase, roles y un superusuario con panel."', 'App v2', 'Firebase Auth/Firestore, 4 roles, panel de superusuario.'],
        ['"Cookie que pida la ubicación para idioma y moneda."', 'App v2', 'Pestaña de cookies y detección por ubicación con consentimiento.'],
        ['Título "Tu cuenta" repetido (prueba propia al hacer capturas).', 'App v2', 'Se eliminó el duplicado.'],
    ], [6, 2, 8], 'Feedback recibido y respuesta')
    d.h1('7. Mejoras aplicadas')
    d.bullets(['Tema claro y ambiente vacacional.', 'Pestañas nuevas: Ofertas, Cookies y privacidad, Recepción, Superusuario.',
               'Validaciones más estrictas (contraseña, sugerencia de correo).', 'Parámetros editables y modo mantenimiento.',
               'Auditoría y reglas de seguridad en el servidor.'])
    d.h1('8. Conclusión')
    d.p('Integrar componentes externos requirió las mismas habilidades que integrar los de otro equipo: leer documentación '
        'ajena, aislar el componente, adaptarlo sin modificarlo y comunicar mejoras de forma constructiva. Cada problema '
        'encontrado dejó una lección aplicable a proyectos futuros.')
    d.h1('9. Ventajas y desventajas de usar componentes externos')
    d.pros_cons(['Ahorro enorme de tiempo', 'Componentes probados por miles de proyectos', 'Licencias libres (Apache, MIT, OFL)', 'Se aprende de código profesional'],
                ['Cambios de versión pueden romper la compilación', 'Menos control sobre errores internos', 'Dependencia de terceros y de sus condiciones'])
    d.tap(10, ['Los componentes externos de UI (Compose, Material 3) se integraron sin perder consistencia.',
              'Ktor y las corrutinas de Kotlin se integraron para no bloquear la app.',
              'Firebase se integró por REST como capa de acceso a datos segura.',
              'La integración externa hizo posible la app móvil multiplataforma.'])
    return d.save()


# ======================================================================================
# E5. APLICACIÓN CON COMPONENTES PROPORCIONADOS + PREGUNTAS DE FEEDBACK
# ======================================================================================
def e5():
    d = Doc('U2_Librerias/U2_E5_Componentes_Proporcionados_y_Preguntas.docx', U, 'Entregable 5', 'Aplicación con los componentes proporcionados',
            'Reutilización de los componentes documentados en tres aplicaciones y cuestionario de retroalimentación')
    d.toc(['Objetivo', 'Componentes proporcionados', 'Aplicaciones construidas con ellos', 'Matriz de reutilización',
           'Cuestionario de retroalimentación', 'Respuestas y análisis', 'Cambios derivados', 'Conclusión', 'Ventajas y desventajas', 'Criterios TAP'])
    d.h1('1. Objetivo')
    d.p('Demostrar que los componentes documentados en el Entregable 2 son realmente reutilizables: con ellos, sin escribir '
        'lógica nueva, se ensamblan tres aplicaciones (Android, iOS y web) y la página informativa reutiliza las mismas '
        'reglas de negocio. Además, se diseña y aplica un cuestionario para obtener retroalimentación sobre su uso.')
    d.h1('2. Componentes proporcionados')
    d.table(['Componente', 'Tipo', 'Documentado en'], [
        ['Pricing, Validation, Format', 'Lógica de dominio', 'E2 §4'], ['HotelRepository + FirebaseAuthApi + FirestoreApi', 'Datos', 'E2 §3.4–3.5, §4'],
        ['Capabilities, rememberLocationRequester', 'Plataforma', 'E2 §4'], ['LumbreButton, Lumi, Stepper, PhotoCard, StatusChip, AnimatedMoney', 'UI', 'E2 §4'],
        ['ConsentBanner, PrivacyScreen, GuardNotice', 'UI de seguridad/privacidad', 'E2 §4'], ['Strings (i18n)', 'Textos en 4 idiomas', 'E1 §10'],
    ], [7, 4.5, 4.5], 'Componentes proporcionados')
    d.h1('3. Aplicaciones construidas con ellos')
    d.table(['Aplicación', 'Punto de entrada', 'Código propio de la plataforma', 'Componentes usados'], [
        ['Android', 'androidApp/MainActivity.kt', '≈ 20 líneas + Location.android.kt', '100 %'],
        ['iOS', 'iosApp + MainViewController', '≈ 10 líneas + Location.ios.kt', '100 %'],
        ['Web (Wasm)', 'webApp/main.kt', '≈ 10 líneas + Location.wasmJs.kt', '100 %'],
        ['Página informativa', 'index.html (JS)', 'Reimplementa Pricing y Validation con las mismas reglas', 'Reglas'],
    ], [3, 4.2, 5.3, 3.5], 'Reutilización por plataforma')
    d.shot('movil_01_inicio.jpg', 'Los mismos componentes en pantalla móvil...', 6.5)
    d.shot('web_03_habitaciones.jpg', '...y en escritorio.', 14)
    d.h1('4. Matriz de reutilización')
    d.table(['Componente', 'Inicio', 'Habitaciones', 'Reserva', 'Reservas', 'Perfil', 'Ofertas', 'Recepción', 'Admin', 'Super'], [
        ['LumbreButton', '✔', '✔', '✔', '✔', '✔', '✔', '✔', '✔', '✔'],
        ['Lumi / LumiSays', '', '', '✔', '✔', '✔', '', '', '', ''],
        ['Stepper', '✔', '', '✔', '', '', '', '', '', ''],
        ['PhotoCard', '✔', '✔', '✔', '', '', '', '', '', ''],
        ['StatusChip', '', '', '', '✔', '', '', '✔', '✔', ''],
        ['AnimatedMoney / money()', '✔', '✔', '✔', '✔', '', '✔', '', '✔', ''],
        ['Pricing.quote', '', '', '✔', '', '', '', '', '', ''],
        ['Validation.*', '', '', '✔', '', '✔', '', '', '✔', '✔'],
        ['GuardNotice', '', '', '', '', '', '', '✔', '✔', '✔'],
    ], [3.6] + [1.38] * 9, 'Uso de componentes por pantalla', 8)
    d.h1('5. Cuestionario de retroalimentación')
    preguntas = [
        ('P1', '¿La documentación (E2) fue suficiente para usar el componente sin preguntar al autor?', 'Escala 1–5'),
        ('P2', '¿Los nombres de parámetros y funciones eran claros?', 'Escala 1–5'),
        ('P3', '¿Encontraste algún caso en el que el componente devolvió un resultado inesperado?', 'Abierta'),
        ('P4', '¿Cuánto tardaste en integrar el componente en una pantalla nueva?', '< 10 min / 10–30 / > 30'),
        ('P5', '¿El componente se ve y se comporta igual en móvil y en web?', 'Sí / No / Parcialmente'),
        ('P6', '¿Qué limitación te afectó más?', 'Abierta'),
        ('P7', '¿Qué parámetro o función añadirías?', 'Abierta'),
        ('P8', '¿Los mensajes de error que devuelven las validaciones son comprensibles para el usuario final?', 'Escala 1–5'),
        ('P9', '¿Recomendarías estos componentes para otro proyecto?', 'Sí / No y por qué'),
        ('P10', 'Como usuario final: ¿completaste una reserva sin ayuda? ¿En cuánto tiempo?', 'Sí/No + tiempo'),
    ]
    d.table(['#', 'Pregunta', 'Tipo de respuesta'], [list(p) for p in preguntas], [1.2, 11, 3.8], 'Cuestionario')
    d.h1('6. Respuestas y análisis')
    d.p('Primera aplicación: el propio equipo respondió el cuestionario al integrar los componentes en las pantallas nuevas '
        '(Ofertas, Recepción, Superusuario y Cookies). Las columnas "Respondente 2" y "Respondente 3" quedan para '
        'aplicarlo a compañeros o usuarios y completar la evaluación.')
    d.table(['Pregunta', 'Equipo (autoevaluación)', 'Respondente 2', 'Respondente 3'], [
        ['P1', '4/5 — faltaba explicar qué significa un resultado nulo.', '', ''],
        ['P2', '5/5', '', ''],
        ['P3', 'Pricing.quote devuelve null si las noches están fuera de rango; ahora está documentado.', '', ''],
        ['P4', '< 10 min para UI (Ofertas usó LumbreButton y money() sin cambios); 10–30 min para el repositorio.', '', ''],
        ['P5', 'Sí: verificado en 375 px y 1280 px.', '', ''],
        ['P6', 'Las pruebas no corren en Node.js por Skiko (se movieron a la JVM).', '', ''],
        ['P7', 'Un Stepper con texto libre.', '', ''],
        ['P8', '5/5 — la sugerencia de correo es lo más útil.', '', ''],
        ['P9', 'Sí: desacoplados y con pruebas.', '', ''],
        ['P10', 'Sí; flujo de 3 pasos.', '', ''],
    ], [1.6, 7.4, 3.5, 3.5], 'Respuestas', 9)
    d.h1('7. Cambios derivados')
    d.bullets(['Documentar en E2 el significado de los valores nulos y de cada clave de error.',
               'Agregar ejemplos de manejo de errores de Firebase (mapError).', 'Eliminar un título duplicado en la sección de cuenta.'])
    d.h1('8. Conclusión')
    d.p('Los componentes cumplieron su propósito: tres aplicaciones comparten el 100 % de la lógica y de la interfaz, y la '
        'retroalimentación confirmó que la documentación permite usarlos de forma autónoma.')
    d.h1('9. Ventajas y desventajas de reutilizar componentes')
    d.pros_cons(['Consistencia visual en todas las pantallas', 'Un error se corrige una sola vez', 'Pantallas nuevas en minutos'],
                ['Un cambio afecta a todas las pantallas que lo usan', 'Hay que documentar bien los parámetros'])
    d.tap(10, ['Los componentes de UI se reutilizan en 3 plataformas con el mismo aspecto.',
              'Los componentes síncronos (Pricing) y asíncronos (repositorio) se probaron por separado.',
              'El repositorio proporcionado concentra todo el acceso a datos.',
              'Las tres apps construidas confirman la propuesta móvil.'])
    return d.save()


# ======================================================================================
# E6. REFLEXIONES Y CONCLUSIONES
# ======================================================================================
def e6():
    d = Doc('U2_Librerias/U2_E6_Reflexiones_y_Conclusiones.docx', U, 'Entregable 6', 'Reflexiones y conclusiones',
            'Lo aprendido al documentar, crear, integrar y evaluar librerías y componentes')
    d.toc(['Resumen del trabajo', 'Reflexión sobre las librerías', 'Reflexión sobre los componentes propios',
           'Reflexión sobre la integración externa', 'Lecciones aprendidas', 'Qué haríamos diferente', 'Trabajo futuro', 'Conclusiones', 'Criterios TAP'])
    d.h1('1. Resumen del trabajo')
    d.table(['Entregable', 'Resultado'], [
        ['E1 Especificaciones', '18 requisitos funcionales, 10 no funcionales, reglas, validaciones, seguridad, casos de uso y diagramas.'],
        ['E2 Librerías y componentes', '9 fichas de librerías externas y 15 componentes propios documentados.'],
        ['E3 Aplicación del equipo', 'App Android, iOS y web publicada, con 14 pantallas y 14 pruebas.'],
        ['E4 Componentes externos', '10 componentes de la web/repositorios integrados; 7 problemas convertidos en oportunidades.'],
        ['E5 Componentes proporcionados', 'Reutilización al 100 % en 3 plataformas y cuestionario de 10 preguntas.'],
    ], [5, 11], 'Resumen')
    d.h1('2. Reflexión sobre las librerías')
    d.p('Elegir una librería es una decisión de arquitectura: condiciona plataformas, rendimiento y mantenimiento. Aprendimos '
        'a revisar la licencia, la fecha del último release y la compatibilidad con el resto de versiones antes de añadirla, '
        'y a fijar versiones en un catálogo central (libs.versions.toml) para que todo el equipo use las mismas.')
    d.h1('3. Reflexión sobre los componentes propios')
    d.p('Separar la lógica (Pricing, Validation) de la interfaz permitió probarla de forma automática y reutilizarla en tres '
        'plataformas. Documentar entradas y salidas obligó a pensar en casos límite (fechas iguales, contraseñas con el '
        'nombre del usuario) que de otro modo habríamos pasado por alto.')
    d.h1('4. Reflexión sobre la integración externa')
    d.p('No contar con componentes de otro equipo no fue una desventaja: integrar componentes de la comunidad nos enfrentó '
        'a documentación real, cambios de versión y limitaciones que no podíamos modificar. La estrategia de envolver cada '
        'componente en una interfaz propia fue clave para mantener el control.')
    d.h1('5. Lecciones aprendidas')
    d.bullets([
        'La seguridad debe vivir en el servidor (reglas de Firestore); el cliente solo mejora la experiencia.',
        'Pedir consentimiento antes de usar la ubicación y usar solo la precisión necesaria genera confianza.',
        'Las pruebas automáticas detectaron traducciones faltantes y errores de cálculo antes que los usuarios.',
        'Leer las notas de versión ahorra horas (AGP 9, yarn.lock de Wasm).',
        'Un diseño agradable (tema claro, fotos, mascota) cambia por completo la percepción de la app.',
    ])
    d.h1('6. Qué haríamos diferente')
    d.bullets(['Definir los roles y la base de datos antes de la interfaz.', 'Escribir las pruebas junto con cada función, no después.',
               'Hacer pruebas con usuarios desde el primer prototipo.'])
    d.h1('7. Trabajo futuro')
    d.bullets(['Pagos con pasarela en modo de prueba.', 'Notificaciones push de llegada.', 'Disponibilidad por habitación física.',
               'Escucha en tiempo real de Firestore.', 'Pruebas de interfaz automatizadas.'])
    d.h1('8. Conclusiones')
    d.p('El proyecto demostró que con librerías bien elegidas y componentes propios bien documentados es posible construir, '
        'sin costo, una aplicación profesional para tres plataformas con cuentas, roles, seguridad y privacidad. La '
        'documentación no fue un trámite final, sino la herramienta que hizo posible reutilizar, integrar y mejorar.')
    d.tap(9, ['Reflexión sobre la calidad de la interfaz y la retroalimentación al usuario.',
              'Lección: separar lo síncrono de lo asíncrono hace la app fluida y fácil de probar.',
              'Lección: la seguridad de los datos debe vivir en el servidor.',
              'Conclusión sobre la viabilidad de la propuesta móvil sin costo.'])
    return d.save()


ALL = [e1, e2, e3, e4, e5, e6]
