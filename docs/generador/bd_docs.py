"""Entregables de la Unidad 4 — Bases de datos (7 documentos)."""
from docgen import Doc, WEB, APPWEB, REPO

U = 'Unidad 4 · Bases de datos'


# ======================================================================================
# 1. CONTEXTO
# ======================================================================================
def contexto():
    d = Doc('U4_BD/U4_1_Contexto.docx', U, 'Entregable U4_1 (Bases de datos)', 'Contexto del problema y propósito de la base de datos',
            'Por qué Lumbre necesita una base de datos y a qué necesidades del sistema responde')
    d.toc(['Resumen', 'Descripción de la organización', 'Problema actual', 'Propósito de la base de datos',
           'Contexto de uso: quién, dónde y cuándo', 'Necesidades del sistema y datos que las satisfacen',
           'Requisitos de datos', 'Volumen y crecimiento estimado', 'Restricciones y supuestos',
           'Indicadores de éxito', 'Relación con los demás entregables', 'Partes interesadas', 'Escenarios de uso del contexto', 'Supuestos del contexto', 'Vista general del contexto', 'Criterios TAP'])

    d.h1('1. Resumen')
    d.p('Lumbre Hotel & Spa es un hotel boutique de 86 habitaciones en la Costa del Sol que recibe huéspedes de México, '
        'Estados Unidos, Europa y Sudamérica. Hasta ahora sus reservas se gestionaban con hojas de cálculo, correos y '
        'llamadas, sin una fuente única de verdad. Este documento explica el problema, el propósito de la base de datos '
        'y el contexto real en el que se usará, y relaciona cada necesidad del sistema con los datos que la resuelven.')
    d.p('La base de datos es el núcleo de la aplicación multiplataforma (Android, iOS y web) construida con Kotlin '
        'Multiplatform: guarda cuentas y roles, el catálogo de habitaciones, promociones, reservas, parámetros del '
        'sistema y un registro de auditoría. Gracias a ella, un huésped puede reservar desde el móvil y ver la misma '
        'reserva en la web, y la recepción la ve al instante.')

    d.h1('2. Descripción de la organización')
    d.table(['Aspecto', 'Detalle'], [
        ['Tipo de negocio', 'Hotel boutique frente al mar, 5 estrellas, con spa, restaurante y excursiones.'],
        ['Capacidad', '86 habitaciones en 3 categorías: Estándar Jardín (2 pax), Suite Deluxe Mar (3 pax) y Ático Lumbre (6 pax).'],
        ['Mercados', 'México, EE. UU., España, Francia, Portugal, Brasil, Colombia y Reino Unido (4 idiomas y 6 monedas).'],
        ['Áreas implicadas', 'Recepción (24 h), administración/comercial, dirección y TI.'],
        ['Canales de venta', 'App Android, app iOS y web (misma aplicación) más la web informativa.'],
    ], [4, 12], 'Perfil de la organización')

    d.h1('3. Problema actual')
    d.p('Antes del sistema, la información estaba dispersa y duplicada. Esto provocaba los siguientes problemas, '
        'observados en la operación diaria:')
    d.table(['Problema', 'Consecuencia', 'Cómo lo resuelve la base de datos'], [
        ['Reservas en hojas de cálculo y correos', 'Sobreventa y reservas perdidas; nadie sabe cuál es la versión buena.', 'Una colección única de reservas con referencia irrepetible (LMB-XXXXXX) y estado controlado.'],
        ['Precios cambiados a mano en varios sitios', 'Presupuestos distintos para la misma estancia.', 'Precio por tipo de habitación y parámetros (impuestos, recargos, descuentos) en un solo lugar.'],
        ['Sin cuentas de cliente', 'El huésped no puede consultar ni cancelar su reserva desde otro dispositivo.', 'Usuarios con perfil en la nube; sus reservas se recuperan al iniciar sesión.'],
        ['Todos pueden cambiar todo', 'Errores y cambios sin responsable.', 'Roles (huésped, recepción, administrador, superusuario) y reglas de acceso en el servidor.'],
        ['Sin historial de cambios', 'Imposible saber quién cambió un precio o canceló una reserva.', 'Tabla de auditoría inmutable con fecha, autor, acción y objetivo.'],
        ['Idioma y moneda fijos', 'Clientes internacionales abandonan la reserva.', 'Preferencias de idioma, moneda y tema guardadas en el perfil.'],
    ], [4.2, 5.4, 6.4], 'Problemas detectados y respuesta de la base de datos', 9)

    d.h1('4. Propósito de la base de datos')
    d.p('Propósito general:', bold_prefix='')
    d.p('Almacenar de forma íntegra, segura y disponible desde cualquier plataforma toda la información necesaria para '
        'vender, gestionar y auditar las estancias del hotel, de modo que cada actor vea solo lo que le corresponde.')
    d.p('Propósitos específicos:')
    d.bullets([
        ('Integridad', 'que una reserva no pueda tener fechas incoherentes, más huéspedes que la capacidad o un estado no válido.'),
        ('Disponibilidad', 'que la misma información esté accesible desde Android, iOS y web en tiempo real.'),
        ('Seguridad y privacidad', 'que cada usuario lea y escriba solo lo permitido por su rol; contraseñas fuera de la base de datos (Firebase Authentication).'),
        ('Trazabilidad', 'registrar quién hizo cada cambio administrativo.'),
        ('Flexibilidad', 'que reglas de negocio como impuestos o noches máximas se cambien sin publicar una nueva versión de la app.'),
        ('Apoyo a decisiones', 'obtener indicadores: reservas activas, ingresos por tipo de habitación, ocupación del día.'),
    ])

    d.h1('5. Contexto de uso: quién, dónde y cuándo')
    d.table(['Actor', 'Dónde', 'Cuándo', 'Qué datos usa'], [
        ['Huésped / visitante', 'Móvil (Android, iOS) o navegador', 'Antes y durante el viaje, a cualquier hora', 'Catálogo, promociones, parámetros (lectura); su perfil y sus reservas (lectura/escritura).'],
        ['Recepción (STAFF)', 'Móvil del turno o PC de recepción', 'Turnos 24 h; picos en llegadas (15:00) y salidas (12:00)', 'Todas las reservas; cambia estados (registro de llegada, cancelación).'],
        ['Administrador (ADMIN)', 'PC de oficina (web)', 'Horario de oficina', 'Precios, disponibilidad, promociones, indicadores.'],
        ['Superusuario (SUPERADMIN)', 'PC de oficina (web)', 'Puntual', 'Usuarios, roles, bloqueo de cuentas, parámetros del sistema, auditoría.'],
        ['Sistema (procesos)', 'Servidores de Firebase', 'Continuo', 'Validación de reglas, autenticación, copias del proveedor.'],
    ], [3.4, 3.6, 3.6, 5.4], 'Contexto de uso por actor', 9)
    d.p('La aplicación aplica una norma de producto: en móvil se hace lo útil sobre la marcha (reservar, consultar, '
        'llave digital y, para el personal, registrar llegadas) y en la web se puede hacer todo (paneles de '
        'administración y superusuario). La base de datos y sus reglas son las mismas para todas las plataformas.')

    d.h1('6. Necesidades del sistema y datos que las satisfacen')
    d.table(['Necesidad del sistema', 'Entidades / datos', 'Operaciones'], [
        ['Mostrar habitaciones y precios actualizados', 'TIPO_HABITACION, AMENIDAD', 'Lectura pública'],
        ['Calcular un presupuesto exacto', 'TIPO_HABITACION, EXTRA, PROMOCION, PARAMETRO', 'Lectura y cálculo en el cliente'],
        ['Reservar y confirmar', 'RESERVA, RESERVA_EXTRA, USUARIO', 'Alta validada por reglas'],
        ['Consultar y cancelar mis reservas', 'RESERVA (filtrada por usuario)', 'Lectura y actualización de estado'],
        ['Recepción del día', 'RESERVA (fechas y estado)', 'Lectura y cambio de estado'],
        ['Gestión comercial', 'TIPO_HABITACION, PROMOCION', 'Actualización por administración'],
        ['Cuentas en cualquier dispositivo', 'USUARIO (preferencias)', 'Lectura/actualización por el propio usuario'],
        ['Control de acceso', 'USUARIO.id_rol, ROL', 'Lectura en cada regla de seguridad'],
        ['Parámetros del negocio', 'PARAMETRO', 'Lectura pública, escritura del superusuario'],
        ['Auditoría', 'AUDITORIA', 'Alta por personal, lectura del superusuario'],
    ], [5.5, 5.5, 5], 'Trazabilidad necesidad → datos', 9)

    d.h1('7. Requisitos de datos')
    d.bullets([
        'Cada reserva tiene una referencia única con formato LMB- más 6 caracteres sin ambigüedades (sin 0/O ni 1/I).',
        'La fecha de salida es posterior a la de llegada; máximo de noches y antelación definidos en PARAMETRO (30 noches y 18 meses por defecto).',
        'Adultos entre 1 y 6, niños entre 0 y 4, y la suma no supera la capacidad del tipo de habitación.',
        'Estados de reserva permitidos: CONFIRMED, CHECKED_IN y CANCELLED.',
        'Correo único por usuario; nombre de 2 a 80 caracteres; teléfono opcional de 7 a 15 dígitos.',
        'Porcentaje de promoción entre 5 y 50; código de 4 a 20 mayúsculas o dígitos.',
        'Precio por noche entre 30 y 5000 EUR (moneda base); las demás monedas se calculan al mostrar.',
        'Ninguna contraseña se guarda en la base de datos: la gestiona el servicio de autenticación.',
        'La auditoría no se puede modificar ni borrar.',
    ])

    d.h1('8. Volumen y crecimiento estimado')
    d.table(['Dato', 'Volumen inicial', 'Crecimiento anual', 'Observación'], [
        ['Usuarios', '~500', '~6 000', 'Huéspedes registrados más personal (≈ 30).'],
        ['Reservas', '~200', '~9 000', '86 hab. × 70 % de ocupación × estancia media de 3 noches.'],
        ['Tipos de habitación', '3', 'Estable', 'Catálogo pequeño y estable.'],
        ['Promociones', '2–10', '~20', 'Campañas por temporada.'],
        ['Auditoría', '0', '~3 000', 'Cambios administrativos.'],
    ], [3.5, 3, 3, 6.5], 'Estimación de volumen', 9)
    d.p('Con este volumen la base de datos cabe holgadamente en el plan gratuito elegido (ver Entregable U4_5): '
        '1 GiB de almacenamiento y 50 000 lecturas y 20 000 escrituras diarias.')

    d.h1('9. Restricciones y supuestos')
    d.bullets([
        ('Costo', 'el proyecto debe funcionar sin pagar licencias ni servidores.'),
        ('Multiplataforma', 'la misma base de datos debe servir a Android, iOS y web sin código distinto por plataforma.'),
        ('Conectividad', 'el huésped puede tener mala conexión; la app conserva una copia local y sincroniza al reconectar.'),
        ('Privacidad', 'se pide el mínimo de datos personales; la ubicación solo se usa para deducir el país y no se almacena.'),
        ('Supuesto', 'la disponibilidad se gestiona por tipo de habitación (no por número físico) en esta versión.'),
    ])

    d.h1('10. Indicadores de éxito')
    d.table(['Indicador', 'Meta'], [
        ['Reservas duplicadas o perdidas', '0'],
        ['Tiempo para ver una reserva nueva en recepción', '< 5 segundos'],
        ['Accesos no autorizados que la base de datos acepte', '0 (las reglas lo impiden en el servidor)'],
        ['Cambios administrativos sin registro de auditoría', '0'],
        ['Costo mensual de la base de datos', '0 € (plan Spark)'],
    ], [10, 6], 'Indicadores')

    d.h1('11. Relación con los demás entregables')
    d.p('Este contexto se representa gráficamente en el diagrama de contexto (U4_2), se modela en el diagrama '
        'entidad-relación (U4_3), justifica los criterios y la elección del sistema gestor (U4_4 y U4_5), se transforma '
        'en el diagrama relacional normalizado (U4_6) y se documenta campo a campo en el diccionario de datos (U4_7).')
    d.p(f'Aplicación funcionando: {APPWEB} · Código: {REPO}')
    d.h1('12. Partes interesadas')
    d.table(['Parte interesada', 'Interés', 'Influencia en los datos'], [
        ['Dirección del hotel', 'Ocupación, ingresos, imagen', 'Define precios, promociones y parámetros'],
        ['Recepción', 'Llegadas sin errores', 'Cambia estados de reserva'],
        ['Huéspedes', 'Reserva rápida, privacidad', 'Crean reservas y perfiles'],
        ['TI / superusuario', 'Seguridad y continuidad', 'Gestiona roles, reglas y auditoría'],
        ['Autoridades (protección de datos)', 'Cumplimiento legal', 'Exigen consentimiento y derecho a borrar datos'],
    ], [4, 5, 7], 'Partes interesadas')
    d.h1('13. Escenarios de uso del contexto')
    for t, txt in (
        ('E1 · Reserva desde el celular', 'Mariana (34, Guadalajara) abre la app un martes en la noche, acepta cookies, ve precios en MXN, reserva 3 noches en Suite Deluxe con desayuno y recibe LMB-XXXXXX. Se crea un documento en reservations con su uid.'),
        ('E2 · Llegada al hotel', 'El viernes a las 15:00 la recepcionista abre Recepción en el móvil del turno, ve a Mariana en "Llegadas de hoy" y registra su llegada: status pasa a CHECKED_IN y se crea un registro en audit.'),
        ('E3 · Ajuste comercial', 'El lunes la administradora sube el precio del Ático de 340 a 360 € desde la web: se actualiza rooms/PENTHOUSE y se audita ROOM_UPDATE; las reservas ya hechas conservan su total.'),
        ('E4 · Temporada alta', 'Dirección pide subir el recargo de fin de semana al 20 %: el superusuario cambia config/params sin publicar una versión nueva.'),
    ):
        d.p(txt, bold_prefix=t + ':')
    d.h1('14. Supuestos del contexto')
    d.table(['#', 'Supuesto', 'Consecuencia en el diseño de la base de datos'], [
        ['S1', 'La disponibilidad se gestiona por tipo de habitación, no por número físico.', 'No existe la entidad HABITACION física; RESERVA referencia a TIPO_HABITACION.'],
        ['S2', 'Una reserva es de un solo tipo de habitación.', 'Relación 1:N TIPO_HABITACION–RESERVA.'],
        ['S3', 'Se puede reservar sin cuenta.', 'RESERVA.id_usuario admite nulo (participación parcial).'],
        ['S4', 'Solo un código promocional por reserva.', 'FK simple codigo_promocion, nula si no hay código.'],
        ['S5', 'El precio aceptado no cambia aunque cambien tarifas.', 'total_eur se almacena (desnormalización controlada).'],
        ['S6', 'Las contraseñas las gestiona Firebase Authentication.', 'Ningún campo de contraseña en la base de datos.'],
        ['S7', 'Los pagos se hacen en el hotel (fuera del alcance).', 'No hay entidades de pago ni factura.'],
        ['S8', 'Todo el personal tiene cuenta individual.', 'La auditoría siempre tiene un autor identificable.'],
        ['S9', 'La ubicación solo sirve para deducir el país y no se guarda.', 'No hay campos de coordenadas; solo idioma y moneda.'],
        ['S10', 'El volumen cabe en el plan gratuito de Firebase.', 'Se elige Firebase (ver U4_4 y U4_5).'],
        ['S11', 'La moneda base es el euro; las demás se calculan al mostrar.', 'Importes en EUR; conversión en la app.'],
        ['S12', 'Los textos del catálogo (fotos, amenidades traducidas) cambian poco.', 'Se guardan en la app; la nube solo guarda precio, capacidad y disponibilidad.'],
    ], [1, 7, 8], 'Supuestos', 9)
    d.h1('15. Vista general del contexto')
    d.diagram('01_contexto.png', 'Diagrama de contexto (detalle en U4_2).', 16)
    d.tap(16, ['Identifica quién usa la interfaz, dónde y cuándo.',
               'Contempla la mala conexión: copia local y sincronización en segundo plano.',
               'Define qué datos necesita cada necesidad del sistema.',
               'Ubica el uso móvil (huésped y recepción) frente al uso web (administración).'])
    return d.save()


# ======================================================================================
# 2. DIAGRAMA DE CONTEXTO
# ======================================================================================
def diagrama_contexto():
    d = Doc('U4_BD/U4_2_Diagrama_de_Contexto.docx', U, 'Entregable U4_2 (Bases de datos)', 'Diagrama de contexto',
            'DFD nivel 0 y nivel 1: el sistema, sus entidades externas, procesos, almacenes y flujos de datos')
    d.toc(['Objetivo', 'Simbología', 'Diagrama de contexto (nivel 0)', 'Entidades externas', 'Flujos de datos del nivel 0',
           'Límite del sistema', 'DFD nivel 1', 'Procesos del nivel 1', 'Almacenes de datos', 'Balanceo entre niveles',
           'Supuestos y restricciones', 'Reglas de construcción aplicadas', 'Criterios TAP'])
    d.h1('1. Objetivo')
    d.p('El diagrama de contexto representa todo el sistema como un único proceso (0) y muestra con quién intercambia '
        'información y qué datos fluyen. Se complementa con el DFD de nivel 1, que abre el proceso 0 en seis procesos y '
        'siete almacenes de datos. Ambos se basan en el contexto (U4_1) y alimentan el modelo E-R (U4_3).')
    d.h1('2. Simbología (notación Yourdon/DeMarco)')
    d.table(['Símbolo', 'Significado', 'Ejemplo en el diagrama'], [
        ['Círculo numerado', 'Proceso (transforma datos)', '0 Sistema de reservas; 3.0 Cotizar y reservar'],
        ['Rectángulo crema', 'Entidad externa humana', 'E1 Huésped, E2 Recepción, E3 Administrador, E4 Superusuario'],
        ['Rectángulo azul', 'Entidad externa sistema/servicio', 'E5 Firebase Auth, E6 Geolocalización, E7 Correo, E8 SO/navegador'],
        ['Rectángulo abierto con Dn', 'Almacén de datos (nivel 1, notación DeMarco)', 'D1 users … D7 almacenamiento local'],
        ['Flecha etiquetada Fn', 'Flujo de datos con sentido', 'F1 datos de reserva'],
    ], [3.5, 5, 7.5], 'Simbología')
    d.h1('3. Diagrama de contexto (nivel 0)')
    d.diagram('01_contexto.png', 'Diagrama de contexto con flujos numerados F1–F14.', 16.5)
    d.h2('3.1 Vista simplificada (se lee desde cualquier caja)')
    d.p('Misma información con el estilo clásico: el sistema en una caja al centro y cada entidad en un rectángulo. '
        'Cada flecha lleva el nombre del dato que viaja y su sentido, así que se puede empezar por cualquier caja: '
        'por ejemplo, desde Recepción se lee "Registro de llegada" hacia el sistema y "Llegadas y salidas del día" de vuelta.')
    d.diagram('01c_contexto_simple.png', 'Diagrama de contexto, vista simplificada.', 16.5)
    d.h1('4. Entidades externas')
    d.table(['Id', 'Entidad', 'Tipo', 'Descripción', 'Frecuencia de interacción'], [
        ['E1', 'Huésped / visitante', 'Persona', 'Explora, cotiza, reserva, consulta y cancela; usa la llave digital en móvil.', 'Diaria, picos en vacaciones'],
        ['E2', 'Recepción (STAFF)', 'Persona', 'Registra llegadas y cancela; consulta las listas del día.', 'Continua (turnos 24 h)'],
        ['E3', 'Administrador (ADMIN)', 'Persona', 'Precios, disponibilidad, promociones e indicadores.', 'Semanal'],
        ['E4', 'Superusuario (SUPERADMIN)', 'Persona', 'Roles, bloqueo de cuentas, parámetros, auditoría.', 'Ocasional'],
        ['E5', 'Firebase Authentication', 'Servicio', 'Alta, inicio de sesión, tokens, verificación y restablecimiento.', 'Cada inicio de sesión y cada hora'],
        ['E6', 'BigDataCloud', 'Servicio', 'País a partir de coordenadas redondeadas.', 'Al aceptar ubicación'],
        ['E7', 'Correo de Firebase', 'Servicio', 'Envía enlaces de verificación y restablecimiento.', 'Al registrarse o recuperar'],
        ['E8', 'SO / navegador', 'Sistema', 'Concede o niega el permiso de ubicación.', 'Una vez por dispositivo'],
    ], [1, 3.4, 1.8, 6.3, 3.5], 'Entidades externas', 8.5)
    d.h1('5. Flujos de datos del nivel 0')
    d.table(['Flujo', 'Origen → destino', 'Contenido (estructura de datos)', 'Ejemplo'], [
        ['F1', 'E1 → 0', 'Datos de reserva = fechas + huéspedes + habitación + extras + código + contacto', '6–9 dic, 2 adultos, DELUXE, BREAKFAST, LUMBRE10, Mariana López'],
        ['F2', 'E1 → 0', 'Consentimiento + credenciales + preferencias', 'Solo necesarias; idioma ES; moneda MXN'],
        ['F3', '0 → E1', 'Presupuesto + referencia + mis reservas + avisos', 'Total MX$14,767; LMB-7MSZSJ'],
        ['F4', 'E2 → 0', 'Cambio de estado = referencia + nuevo estado', 'LMB-7QK2PA → CHECKED_IN'],
        ['F5', '0 → E2', 'Listas del día (llegadas, en el hotel, salidas)', '2 huéspedes en el hotel'],
        ['F6', 'E3 → 0', 'Catálogo = tipo + precio + disponibilidad; promoción', 'PENTHOUSE 360 €; VERANO15 15 %'],
        ['F7', '0 → E3', 'Indicadores = activas + ingresos + ocupación + ticket medio', '5 activas; MX$97,988'],
        ['F8', 'E4 → 0', 'Gobierno = rol / bloqueo / parámetros', 'usuario → STAFF; recargo 20 %'],
        ['F9', '0 → E4', 'Usuarios + auditoría + estado de seguridad', '300 registros recientes'],
        ["F10 / F10'", '0 ↔ E5', 'Correo + contraseña → UID + idToken (1 h) + refreshToken', 'uid kQ3…Zp2'],
        ["F11 / F11'", '0 ↔ E6', 'lat/lon con 1 decimal → código ISO', '19.7, −101.2 → MX'],
        ['F12', 'E5 → E7', 'Solicitud de correo', 'VERIFY_EMAIL'],
        ['F13', 'E7 → E1', 'Correo con enlace', 'Verifica tu correo'],
        ["F14 / F14'", '0 ↔ E8', 'Solicitud de permiso → coordenadas o rechazo', 'Permitir / Bloquear'],
    ], [1.6, 2.2, 6.6, 5.6], 'Flujos del nivel 0', 8.5)
    d.h1('6. Límite del sistema')
    d.p('Dentro del proceso 0 quedan las interfaces de Android, iOS y web, las reglas de negocio (presupuesto, '
        'validaciones, roles), la sincronización y la base de datos Firebase Cloud Firestore con sus reglas de seguridad. '
        'La base de datos se considera parte del sistema porque el equipo diseña su estructura y sus reglas; Firebase '
        'Authentication, el correo y la geolocalización son servicios externos que no controlamos.')
    d.h1('7. DFD nivel 1')
    d.diagram('01b_dfd_nivel1.png', 'DFD nivel 1: seis procesos y siete almacenes.', 16.5)
    d.h1('8. Procesos del nivel 1')
    d.table(['Proceso', 'Entradas', 'Salidas', 'Lógica principal'], [
        ['1.0 Gestionar cuenta y sesión', 'Credenciales, perfil, UID/tokens', 'Perfil en D1, token en D7', 'Registro como GUEST, bloqueo tras 5 fallos, renovación de token'],
        ['2.0 Consentimiento, idioma y moneda', 'Elección de cookies, país', 'Preferencias en D7', 'Solo pide ubicación si el usuario la activa; redondea coordenadas'],
        ['3.0 Cotizar y reservar', 'Fechas, huéspedes, extras, código; D2, D3, D5', 'Reserva en D4 y D7; presupuesto', 'Pricing.quote, validaciones, cooldown, referencia única'],
        ['4.0 Operar recepción', 'Acción de recepción; D4', 'Estado en D4; registro en D6', 'Filtra llegadas/en hotel/salidas por fecha'],
        ['5.0 Administrar catálogo', 'Precio, disponibilidad, promo; D4', 'D2, D3, D6; indicadores', 'Rangos 30–5000 € y 5–50 %'],
        ['6.0 Gobernar y auditar', 'Rol, bloqueo, parámetros; D6', 'D1, D5, D6; listados', 'Solo SUPERADMIN; no puede cambiarse a sí mismo'],
    ], [3.4, 4, 3.6, 5], 'Procesos', 8.5)
    d.h1('9. Almacenes de datos')
    d.table(['Almacén', 'Implementación', 'Contenido', 'Procesos que lo usan'], [
        ['D1 users', 'Firestore users/{uid}', 'Perfil, rol, preferencias', '1.0, 6.0'],
        ['D2 rooms', 'Firestore rooms/{id}', 'Precio, capacidad, disponibilidad', '3.0, 5.0'],
        ['D3 promos', 'Firestore promos/{code}', 'Códigos y porcentaje', '3.0, 5.0'],
        ['D4 reservations', 'Firestore reservations/{ref}', 'Reservas', '3.0, 4.0, 5.0'],
        ['D5 config/params', 'Firestore config/params', 'Reglas de negocio', '3.0, 6.0'],
        ['D6 audit', 'Firestore audit/{autoId}', 'Registro inmutable', '4.0, 5.0, 6.0'],
        ['D7 almacenamiento local', 'multiplatform-settings', 'Token, preferencias, copia de reservas', '1.0, 2.0, 3.0'],
    ], [3.2, 4.4, 4.6, 3.8], 'Almacenes', 9)
    d.h1('10. Balanceo entre niveles')
    d.p('Cada flujo del nivel 0 aparece en el nivel 1: F1–F3 en los procesos 2.0 y 3.0; F4–F5 en 4.0; F6–F7 en 5.0; '
        'F8–F9 en 6.0; F10 en 1.0; F11 y F14 en 2.0. Ningún flujo nuevo cruza el límite del sistema en el nivel 1.')
    d.h1('11. Supuestos y restricciones')
    d.table(['#', 'Supuesto / restricción'], [
        ['1', 'El personal usa cuentas individuales; no hay cuentas compartidas.'],
        ['2', 'Todos los servicios externos usados son gratuitos y no requieren tarjeta.'],
        ['3', 'Firebase Authentication es la única fuente de identidad; la app nunca guarda contraseñas.'],
        ['4', 'El correo lo envía Firebase; el sistema solo lo solicita (por eso F12 va de E5 a E7).'],
        ['5', 'Si no hay conexión, los procesos 2.0 y 3.0 funcionan con D7 y sincronizan después.'],
        ['6', 'Los pagos no forman parte del sistema en esta versión.'],
        ['7', 'Las coordenadas nunca se almacenan (no hay almacén para ellas).'],
    ], [1, 15], 'Supuestos')
    d.h1('12. Reglas de construcción aplicadas')
    d.bullets(['Un solo proceso en el nivel 0, numerado 0.', 'Flujos nombrados con sustantivos (datos), no con verbos.',
               'Ningún flujo directo entre entidades externas salvo el correo, que origina el servicio de Firebase.',
               'Cada entrada produce al menos una salida al actor.', 'Los mismos nombres se usan en el E-R y en el diccionario.'])
    d.tap(13, ['Los flujos F1–F9 corresponden a pantallas concretas de la interfaz.',
               'Los flujos F10, F11 y F14 son asíncronos (red y permisos) y no bloquean la UI.',
               'El nivel 1 muestra exactamente qué proceso lee y escribe cada almacén.',
               'E1 y E2 usan el móvil; E3 y E4 la web (norma del producto).'])
    return d.save()


# ======================================================================================
# 3. DIAGRAMA ENTIDAD-RELACIÓN
# ======================================================================================
def diagrama_er():
    d = Doc('U4_BD/U4_3_Diagrama_Entidad_Relacion.docx', U, 'Entregable U4_3 (Bases de datos)', 'Diagrama entidad-relación',
            'Entidades, atributos, claves, relaciones y cardinalidades del problema')
    d.toc(['Método seguido', 'Diagrama E-R', 'Entidades y atributos', 'Relaciones y cardinalidades',
           'Reglas de negocio que justifican las cardinalidades', 'Resolución de relaciones N:M',
           'Atributos calculados y derivados', 'Validación del modelo con casos reales', 'Cómo leer la notación de Chen', 'Ciclo de vida de RESERVA', 'Supuestos del modelo', 'Ventajas y desventajas de cada notación', 'Criterios TAP'])
    d.h1('1. Método seguido')
    d.bullets([
        'Se extrajeron sustantivos del contexto (U4_1) y de los casos de uso: usuario, rol, habitación, reserva, extra, promoción, parámetro, auditoría, amenidad.',
        'Se descartaron conceptos que son atributos (idioma, moneda, estado) o que no se almacenan (ubicación exacta).',
        'Se identificó la clave primaria de cada entidad priorizando identificadores naturales estables (código de promoción, referencia de reserva).',
        'Se definieron relaciones con su cardinalidad mínima y máxima a partir de reglas de negocio verificables.',
        'Se validó el modelo recorriendo escenarios reales (sección 8).',
    ], numbered=True)
    d.h1('2. Diagrama E-R')
    d.h2('2.1 Notación de Chen (rectángulos, rombos y óvalos)')
    d.p('Diagrama principal. Cada rectángulo es una entidad, cada rombo una relación entre exactamente dos entidades y '
        'cada óvalo un atributo. Se entiende empiece donde empiece la lectura: cualquier entidad lleva a sus relaciones '
        'y de ahí a la otra entidad, con la cardinalidad escrita sobre cada línea. Versión ampliable sin pérdida de calidad: '
        'https://jancarliux24.github.io/hotel-lumbre/diagramas/#02a_er_chen')
    d.diagram('02a_er_chen.png', 'Modelo E-R conceptual en notación de Chen.', 16.5)
    d.h2('2.2 Notación pata de gallo (modelo lógico)')
    d.diagram('02_entidad_relacion.png', 'Modelo entidad-relación lógico (notación pata de gallo).', 13.5)
    d.p('Lectura de la notación: | significa "uno", o significa "cero" (opcional) y la pata de gallo significa "muchos". '
        'Por ejemplo, ROL ||--o{ USUARIO se lee "un rol se asigna a cero o muchos usuarios; cada usuario tiene exactamente un rol".')
    d.h1('3. Entidades y atributos')
    rows = [
        ['ROL', 'Perfil de permisos.', 'id_rol', 'nombre (GUEST, STAFF, ADMIN, SUPERADMIN), nivel (0–3)'],
        ['USUARIO', 'Persona con cuenta.', 'id_usuario (UID de Firebase)', 'correo (único), nombre, teléfono, idioma, moneda, tema, bloqueado, fecha_alta, último_acceso'],
        ['TIPO_HABITACION', 'Categoría vendible.', 'id_tipo', 'nombre, descripción, superficie_m2, capacidad, precio_noche_eur, disponible'],
        ['AMENIDAD', 'Comodidad ofrecida.', 'id_amenidad', 'nombre'],
        ['PROMOCION', 'Código de descuento.', 'código', 'porcentaje, activa'],
        ['RESERVA', 'Estancia contratada.', 'referencia (LMB-XXXXXX)', 'nombre_huésped, correo_contacto, teléfono_contacto, fecha_llegada, fecha_salida, adultos, niños, total_eur, estado, notas, fecha_creación'],
        ['EXTRA', 'Servicio adicional.', 'id_extra', 'nombre, precio_eur, unidad_cobro'],
        ['PARAMETRO', 'Regla configurable.', 'clave', 'valor, descripción'],
        ['AUDITORIA', 'Registro de cambio.', 'id_auditoria', 'fecha_hora, acción, objetivo'],
    ]
    d.table(['Entidad', 'Descripción', 'Clave primaria', 'Atributos'], rows, [3, 3.2, 3.3, 6.5], 'Entidades del modelo', 9)
    d.note('Los datos de contacto se repiten en RESERVA a propósito: la reserva puede hacerla un visitante sin cuenta o '
           'una persona para un tercero, y el contacto debe conservarse aunque el usuario cambie su perfil. No es una '
           'redundancia sino un dato histórico de la reserva.', 'Decisión de diseño')
    d.h1('4. Relaciones y cardinalidades')
    d.table(['Relación', 'Entidades', 'Cardinalidad', 'Participación', 'Lectura'], [
        ['asigna', 'ROL – USUARIO', '1 : N', 'Total en USUARIO', 'Todo usuario tiene exactamente un rol; un rol lo tienen 0..N usuarios.'],
        ['realiza', 'USUARIO – RESERVA', '0..1 : N', 'Parcial en RESERVA', 'Una reserva puede no tener usuario (visitante); un usuario hace 0..N reservas.'],
        ['se reserva en', 'TIPO_HABITACION – RESERVA', '1 : N', 'Total en RESERVA', 'Toda reserva es de un único tipo; un tipo aparece en 0..N reservas.'],
        ['se aplica a', 'PROMOCION – RESERVA', '0..1 : N', 'Parcial en RESERVA', 'Una reserva usa como máximo un código.'],
        ['incluye', 'RESERVA – EXTRA', 'N : M', 'Parcial en ambas', 'Una reserva incluye 0..N extras; un extra está en 0..N reservas.'],
        ['ofrece', 'TIPO_HABITACION – AMENIDAD', 'N : M', 'Parcial en ambas', 'Cada tipo ofrece varias amenidades y cada amenidad puede estar en varios tipos.'],
        ['genera', 'USUARIO – AUDITORIA', '1 : N', 'Total en AUDITORIA', 'Todo registro tiene un autor.'],
        ['modifica', 'USUARIO – PARAMETRO', '0..1 : N', 'Parcial', 'Se guarda quién cambió por última vez cada parámetro.'],
    ], [2.3, 3.6, 2, 2.6, 5.5], 'Relaciones', 9)
    d.h1('5. Reglas de negocio que justifican las cardinalidades')
    d.bullets([
        'RN-01: una reserva corresponde a un solo tipo de habitación (si el cliente quiere dos, hace dos reservas).',
        'RN-02: se permite reservar sin cuenta; al iniciar sesión, las reservas locales se asocian al usuario.',
        'RN-03: solo se acepta un código promocional por reserva; los descuentos automáticos (larga estancia) no son códigos.',
        'RN-04: el rol es obligatorio; al registrarse, todo usuario nace como GUEST y solo el superusuario puede cambiarlo.',
        'RN-05: cada cambio administrativo genera un registro de auditoría con su autor.',
    ])
    d.h1('6. Resolución de relaciones N:M')
    d.p('Las dos relaciones N:M se transforman en el modelo relacional (U4_6) en tablas asociativas: RESERVA_EXTRA '
        '(con el atributo propio importe_eur, que congela el precio cobrado) y TIPO_HABITACION_AMENIDAD.')
    d.h1('7. Atributos calculados y derivados')
    d.table(['Atributo', 'Se calcula a partir de', '¿Se almacena?'], [
        ['noches', 'fecha_salida − fecha_llegada', 'No (se deriva).'],
        ['total_eur', 'precio_noche, noches, recargo fin de semana, extras, descuentos, impuestos', 'Sí: congela el precio aceptado aunque luego cambien tarifas.'],
        ['ocupación del día', 'reservas con llegada ≤ hoy < salida', 'No.'],
    ], [3.5, 8, 4.5], 'Atributos derivados')
    d.h1('8. Validación del modelo con casos reales')
    d.table(['Escenario', 'Recorrido en el modelo', 'Resultado'], [
        ['Visitante reserva sin cuenta', 'RESERVA sin USUARIO, con TIPO_HABITACION y EXTRA', 'Válido (relación 0..1).'],
        ['Huésped aplica LUMBRE10', 'RESERVA → PROMOCION', 'Válido (máximo un código).'],
        ['Recepción registra llegada', 'RESERVA.estado = CHECKED_IN, AUDITORIA nueva', 'Válido, con autor.'],
        ['Superusuario sube a alguien a ADMIN', 'USUARIO.id_rol cambia; AUDITORIA registra', 'Válido.'],
    ], [4.5, 7, 4.5], 'Validación por escenarios')
    d.h1('9. Cómo leer la notación de Chen')
    d.p('El mismo modelo en notación de Chen: rectángulos = entidades, rombos = relaciones, óvalos = atributos '
        '(subrayado = clave, punteado = derivado, con ramas = compuesto), línea doble = participación total, círculo con 1/N/M = cardinalidad. '
        'Se lee igual desde cualquier entidad: cada rombo une exactamente dos entidades y cada atributo sale en su propio rayo, sin cruces.')
    d.p('El diagrama completo está en la sección 2.1.')
    d.h1('10. Ciclo de vida de la entidad RESERVA')
    d.diagram('17_estados_reserva.png', 'Estados permitidos de una reserva.', 12)
    d.h1('11. Supuestos del modelo')
    d.bullets(['Disponibilidad por tipo de habitación (no por número).', 'Un código promocional como máximo por reserva.',
               'Visitantes sin cuenta pueden reservar.', 'La auditoría siempre tiene autor.', 'Las amenidades y extras son catálogos estables.'])
    d.h1('12. Ventajas y desventajas de cada notación')
    d.h2('Notación de Chen')
    d.pros_cons(['Muestra atributos, relaciones y cardinalidad de forma visual', 'Fácil de explicar a personas no técnicas',
                 'Distingue atributos clave, derivados y compuestos'],
                ['Ocupa mucho espacio con muchos atributos', 'No muestra tipos de dato ni claves foráneas'])
    d.h2('Notación pata de gallo')
    d.pros_cons(['Compacta: atributos dentro de la entidad', 'Muestra cardinalidad mínima y máxima en la línea', 'Cercana al modelo relacional'],
                ['Menos intuitiva para quien no conoce los símbolos', 'Las relaciones N:M no tienen nombre visible tan claro'])
    d.tap(13, ['Las entidades corresponden a pantallas (habitaciones, reservas, perfil, paneles).',
               'El estado de RESERVA se actualiza de forma asíncrona y se refleja en la UI.',
               'Las relaciones definen qué consultas hará la app (mis reservas, llegadas del día).',
               'USUARIO y RESERVA son el núcleo del uso móvil.'])
    return d.save()


# ======================================================================================
# 4. CRITERIOS DE SELECCIÓN
# ======================================================================================
CANDIDATOS = ['Firebase (Cloud Firestore + Authentication)', 'PostgreSQL (Supabase)', 'MySQL 8 (autoalojado)', 'SQL Server Express', 'MongoDB Atlas', 'SQLite']


def criterios():
    d = Doc('U4_BD/U4_4_Criterios_de_Seleccion_SMBD.docx', U, 'Entregable U4_4 (Bases de datos)', 'Criterios de selección de un SMBD',
            'Análisis técnico, económico, de seguridad, escalabilidad, compatibilidad y facilidad de uso')
    d.toc(['Requisitos que condicionan la elección', 'Criterios y su peso', 'Candidatos evaluados',
           'Análisis por criterio', 'Matriz de decisión ponderada', 'Riesgos y mitigaciones', 'Conclusión', 'Relacional frente a NoSQL', 'Ventajas y desventajas de cada candidato', 'Costos', 'Criterios TAP'])
    d.h1('1. Requisitos que condicionan la elección')
    d.bullets([
        ('R1 Costo cero', 'sin licencias ni servidores de pago.'),
        ('R2 Multiplataforma', 'acceso igual desde Android, iOS y navegador (Kotlin/Wasm) sin controladores nativos.'),
        ('R3 Seguridad por rol en el servidor', 'el cliente no es de confianza; las reglas deben aplicarse en el servidor.'),
        ('R4 Autenticación integrada', 'cuentas con correo y contraseña, verificación y recuperación.'),
        ('R5 Tiempo real y uso sin conexión tolerante', 'recepción ve reservas nuevas en segundos.'),
        ('R6 Escalabilidad', 'crecer de cientos a decenas de miles de reservas sin rediseño.'),
        ('R7 Facilidad de operación', 'equipo pequeño, sin administrador de bases de datos dedicado.'),
    ])
    d.h1('2. Criterios y su peso')
    d.table(['Criterio', 'Qué se evalúa', 'Peso'], [
        ['Técnico', 'Modelo de datos, consultas, transacciones, acceso desde Wasm/móvil.', '20 %'],
        ['Económico', 'Costo de licencia, alojamiento y plan gratuito suficiente.', '20 %'],
        ['Seguridad', 'Control de acceso por usuario/rol en servidor, cifrado, auditoría.', '20 %'],
        ['Escalabilidad', 'Crecimiento horizontal, límites, rendimiento.', '15 %'],
        ['Compatibilidad', 'SDK/REST para Kotlin Multiplatform, Android, iOS y web.', '15 %'],
        ['Facilidad de uso', 'Curva de aprendizaje, consola, documentación, mantenimiento.', '10 %'],
    ], [3, 10, 3], 'Criterios ponderados (suman 100 %)')
    d.h1('3. Candidatos evaluados')
    d.table(['Candidato', 'Tipo', 'Plan gratuito'], [
        ['Firebase (Cloud Firestore + Authentication)', 'NoSQL documental gestionado', 'Spark: 1 GiB, 50 000 lecturas y 20 000 escrituras/día, sin tarjeta'],
        ['PostgreSQL (Supabase)', 'Relacional gestionado', '500 MB, proyecto pausado tras inactividad'],
        ['MySQL 8 (autoalojado)', 'Relacional', 'Gratis, pero requiere servidor propio (costo de hosting)'],
        ['SQL Server Express', 'Relacional', 'Gratis hasta 10 GB; Windows/servidor propio'],
        ['MongoDB Atlas', 'NoSQL documental gestionado', 'M0: 512 MB'],
        ['SQLite', 'Relacional embebido', 'Gratis, solo local (no sincroniza entre dispositivos)'],
    ], [4.5, 4.5, 7], 'Candidatos')
    d.h1('4. Análisis por criterio')
    d.h2('4.1 Técnico')
    d.p('Las opciones relacionales (PostgreSQL, MySQL, SQL Server) ofrecen integridad referencial y SQL completo, '
        'ideales para el modelo normalizado. Firestore ofrece documentos con consultas por índice, transacciones y '
        'actualizaciones en tiempo real, suficiente para las consultas del hotel (reservas de un usuario, del día o '
        'por estado). SQLite no comparte datos entre dispositivos, lo que incumple R2.')
    d.h2('4.2 Económico')
    d.p('Firestore y Supabase tienen planes gratuitos reales; MySQL y SQL Server son gratuitos como software pero '
        'necesitan un servidor siempre encendido (costo mensual). MongoDB Atlas M0 es gratuito pero con menos capacidad.')
    d.h2('4.3 Seguridad')
    d.p('Firestore aplica reglas declarativas en el servidor que evalúan el token del usuario y su rol en cada lectura '
        'y escritura; Supabase ofrece Row Level Security equivalente en PostgreSQL. Las opciones autoalojadas exigen '
        'construir y mantener una API propia con autenticación, lo que aumenta la superficie de ataque.')
    d.h2('4.4 Escalabilidad')
    d.p('Firestore escala automáticamente sin administrar instancias. PostgreSQL gestionado escala verticalmente y '
        'requiere planes de pago al crecer. MySQL y SQL Server autoalojados dependen del servidor contratado.')
    d.h2('4.5 Compatibilidad')
    d.p('Firestore y Firebase Authentication tienen API REST documentadas, consumibles con Ktor desde Kotlin '
        'Multiplatform en Android, iOS y Wasm sin SDK nativo. Supabase también tiene REST (PostgREST). Los motores '
        'autoalojados no exponen REST por sí mismos.')
    d.h2('4.6 Facilidad de uso')
    d.p('Firebase ofrece consola web con editor de datos y de reglas, autenticación lista y documentación extensa; '
        'el equipo ya lo conoce de proyectos anteriores. PostgreSQL requiere más conocimiento de administración.')
    d.h1('5. Matriz de decisión ponderada')
    pesos = [0.20, 0.20, 0.20, 0.15, 0.15, 0.10]
    notas = {
        'Firebase (Cloud Firestore + Authentication)': [4, 5, 5, 5, 5, 5],
        'PostgreSQL (Supabase)': [5, 4, 5, 4, 4, 4],
        'MySQL 8 (autoalojado)': [5, 2, 3, 3, 2, 3],
        'SQL Server Express': [5, 2, 3, 2, 2, 3],
        'MongoDB Atlas': [4, 4, 4, 4, 3, 4],
        'SQLite': [3, 5, 2, 1, 2, 5],
    }
    rows = []
    for c in CANDIDATOS:
        n = notas[c]
        total = sum(a * b for a, b in zip(n, pesos))
        rows.append([c] + [str(x) for x in n] + [f'{total:.2f}'])
    rows.sort(key=lambda r: -float(r[-1]))
    d.table(['Candidato', 'Téc. 20 %', 'Econ. 20 %', 'Seg. 20 %', 'Escal. 15 %', 'Compat. 15 %', 'Uso 10 %', 'Total (/5)'],
            rows, [4.2, 1.6, 1.6, 1.6, 1.7, 1.8, 1.5, 1.8], 'Matriz de decisión (escala 1 a 5)', 9)
    d.p('Firebase obtiene la mayor puntuación (4.80) gracias a costo cero, seguridad en el servidor y compatibilidad '
        'multiplataforma; PostgreSQL en Supabase queda muy cerca (4.40) y se conserva como alternativa de migración.')
    d.h1('6. Riesgos y mitigaciones')
    d.table(['Riesgo', 'Mitigación'], [
        ['Sin integridad referencial nativa en NoSQL', 'Reglas de Firestore que validan tipos, rangos y relaciones; validación duplicada en el cliente.'],
        ['Superar el plan gratuito', 'Consultas filtradas por usuario, caché local; alertas de uso en la consola.'],
        ['Dependencia de proveedor', 'Modelo relacional documentado (U4_6) y DDL listo para PostgreSQL; repositorio de datos aislado en el código.'],
    ], [6, 10], 'Riesgos')
    d.h1('7. Conclusión')
    d.p('Los criterios técnicos, económicos, de seguridad, escalabilidad, compatibilidad y facilidad de uso apuntan a '
        'un SMBD gestionado con seguridad declarativa en servidor y acceso REST multiplataforma. Por eso el SMBD '
        'seleccionado es Firebase (Cloud Firestore + Authentication); la justificación detallada está en el Entregable U4_5.')
    d.h1('8. Relacional frente a NoSQL documental')
    d.table(['Aspecto', 'Relacional (PostgreSQL, MySQL)', 'NoSQL documental (Firebase Firestore)'], [
        ['Estructura', 'Tablas con esquema fijo', 'Colecciones de documentos JSON con esquema flexible'],
        ['Integridad', 'FK y CHECK en el motor', 'Reglas de seguridad + validación en la app'],
        ['Consultas', 'SQL completo, JOIN', 'Consultas por campo e índices; sin JOIN (se desnormaliza)'],
        ['Transacciones', 'ACID completas', 'Transacciones y escrituras por lotes atómicas'],
        ['Escalado', 'Vertical (más servidor)', 'Horizontal automático'],
        ['Acceso desde la app', 'Requiere API propia', 'REST/SDK directo con reglas'],
        ['Tiempo real', 'Requiere componentes extra', 'Integrado'],
    ], [3.2, 6.2, 6.6], 'Comparativa de paradigmas', 9)
    d.h1('9. Ventajas y desventajas de cada candidato')
    pc = {
        'Firebase (Cloud Firestore + Authentication)': (
            ['Plan gratuito real sin tarjeta', 'Cuentas, verificación y recuperación incluidas', 'Reglas de seguridad en el servidor',
             'REST desde Android, iOS y web', 'Escala solo; sin servidores que mantener', 'Consola visual para revisar datos'],
            ['Sin JOIN ni integridad referencial nativa', 'Consultas complejas/analíticas limitadas', 'Dependencia de Google (lock-in)',
             'Costo por operación si se supera la cuota', 'Sin respaldos automáticos en el plan gratuito']),
        'PostgreSQL (Supabase)': (
            ['SQL completo, JOIN e integridad referencial', 'Row Level Security por usuario', 'API REST automática', 'Código abierto: se puede migrar a otro PostgreSQL'],
            ['El proyecto gratuito se pausa tras días sin uso', '500 MB en el plan gratuito', 'Plan Pro de pago al crecer', 'Menos material en español para KMP']),
        'MySQL 8 (autoalojado)': (
            ['Muy conocido y documentado', 'SQL completo', 'Control total del servidor'],
            ['Requiere servidor siempre encendido (costo mensual)', 'Hay que programar API, autenticación y seguridad', 'Mantenimiento y respaldos a cargo del equipo']),
        'SQL Server Express': (
            ['Herramientas visuales maduras', 'Gratis hasta 10 GB'],
            ['Requiere Windows/servidor propio', 'Límite de 10 GB y de recursos', 'Sin API REST ni autenticación integradas']),
        'MongoDB Atlas': (
            ['Documental y flexible como Firestore', 'Consultas y agregaciones potentes', 'Plan M0 gratuito'],
            ['Solo 512 MB gratis', 'Requiere backend propio para reglas por usuario desde la app', 'Sin autenticación de usuarios integrada']),
        'SQLite': (
            ['Gratis, sin servidor, muy rápido', 'Ideal para datos locales'],
            ['No comparte datos entre dispositivos', 'Sin control de acceso por usuario', 'No sirve para recepción ni administración']),
    }
    for cand, (pros, cons) in pc.items():
        d.h2(cand)
        d.pros_cons(pros, cons)
    d.h1('10. Costos')
    d.note('Precios de referencia en USD, aproximados y sujetos a cambio por cada proveedor; verificar en la página oficial '
           'antes de usarlos en una propuesta económica.', 'Aviso')
    d.h2('10.1 Costo del SMBD')
    d.table(['Opción', 'Plan gratuito', 'Al crecer', 'Costo estimado para Lumbre'], [
        ['Firebase (Spark → Blaze)', '1 GiB, 50 000 lecturas y 20 000 escrituras al día; Auth sin costo para correo/contraseña',
         'Pago por uso (centavos por cada 100 000 operaciones) conservando la cuota gratuita', 'Año 1: 0 USD · Año 3 (≈ 3× uso): 0–5 USD/mes'],
        ['PostgreSQL (Supabase)', '500 MB; el proyecto se pausa por inactividad', 'Plan Pro ≈ 25 USD/mes', 'Año 1: 0 USD (con pausas) · producción: ≈ 300 USD/año'],
        ['MySQL / PostgreSQL autoalojado', 'Software gratis', 'Servidor virtual (VPS) ≈ 5–12 USD/mes + horas de mantenimiento', '≈ 60–150 USD/año + tiempo del equipo'],
        ['SQL Server Express', 'Licencia gratis (≤ 10 GB)', 'Servidor Windows ≈ 15–30 USD/mes', '≈ 180–360 USD/año'],
        ['MongoDB Atlas', 'M0: 512 MB', 'Planes de pago desde ≈ 8–60 USD/mes', '≈ 100–700 USD/año'],
        ['SQLite', 'Gratis', '—', '0 USD (pero no cumple los requisitos)'],
    ], [3.6, 4.4, 4.2, 3.8], 'Costo del gestor de base de datos', 8.5)
    d.h2('10.2 Costo de hosting de la aplicación web')
    d.table(['Opción', 'Costo', 'Ventajas', 'Desventajas'], [
        ['GitHub Pages (elegido)', '0 USD', 'Se publica solo con cada push (GitHub Actions); HTTPS incluido', 'Solo archivos estáticos; límites de tamaño y transferencia mensual'],
        ['Firebase Hosting', '0 USD (Spark, con cuota diaria)', 'CDN de Google; mismo proyecto que la base de datos', 'Cuota de transferencia diaria en el plan gratuito'],
        ['Netlify / Vercel', '0 USD (planes personales)', 'Despliegue sencillo, vistas previas', 'Restricciones de uso comercial o por créditos en planes gratuitos'],
        ['Servidor propio (VPS)', '≈ 5–12 USD/mes', 'Control total', 'Mantenimiento, seguridad y certificados a cargo del equipo'],
        ['Dominio propio (opcional)', '≈ 10–15 USD/año', 'Dirección profesional (lumbrehotel.com)', 'Costo anual y renovación'],
    ], [3.4, 2.8, 5, 4.8], 'Hosting web', 8.5)
    d.h2('10.3 Costo de distribución de la app móvil')
    d.table(['Canal', 'Costo', 'Comentario'], [
        ['APK directo (actual)', '0 USD', 'Se descarga desde la web; Android pide permitir "orígenes desconocidos".'],
        ['Google Play', '≈ 25 USD, pago único', 'Instalación con un toque, actualizaciones automáticas, revisión de Google.'],
        ['App Store (iPhone)', '≈ 99 USD/año', 'Obligatorio para distribuir en iPhone; requiere Mac para compilar.'],
    ], [4, 3.5, 8.5], 'Distribución móvil')
    d.h2('10.4 Costo total estimado')
    d.table(['Escenario', 'Año 1', 'Años siguientes'], [
        ['Actual (Firebase Spark + GitHub Pages + APK)', '0 USD', '0 USD'],
        ['Con dominio y Google Play', '≈ 35–40 USD', '≈ 10–15 USD/año'],
        ['Con dominio, Google Play y App Store', '≈ 135–140 USD', '≈ 110–115 USD/año'],
        ['Alternativa: PostgreSQL en VPS + dominio', '≈ 70–165 USD + mantenimiento', 'Igual cada año'],
    ], [8, 4, 4], 'Costo total de propiedad')
    d.tap(11, ['Los criterios priorizan respuestas rápidas para una interfaz fluida.',
              'Se valora el acceso no bloqueante (REST asíncrono) desde corrutinas.',
              'Se evalúan seguridad, integridad y costo del acceso a datos.',
              'Se exige compatibilidad con Android, iOS y web.'])
    return d.save()


# ======================================================================================
# 5. ELECCIÓN
# ======================================================================================
def eleccion():
    d = Doc('U4_BD/U4_5_Eleccion_del_SMBD_Firebase.docx', U, 'Entregable U4_5 (Bases de datos)', 'Elección del SMBD: Firebase',
            'Por qué Firebase (Cloud Firestore + Authentication) es el SMBD del proyecto y cómo se implementó')
    d.toc(['Decisión', 'Justificación frente a cada requisito', 'Cómo se implementó', 'Del modelo relacional a colecciones',
           'Reglas de seguridad en el servidor', 'Límites del plan gratuito y uso previsto', 'Plan de migración', 'Evidencia', 'Modelo de datos NoSQL en Firebase', 'Cómo protege Firebase cada operación', 'Acceso a datos desde la app', 'Ventajas y desventajas de Firebase', 'Criterios TAP'])
    d.h1('1. Decisión')
    d.p('El sistema gestor de base de datos (SMBD) elegido para Lumbre Hotel & Spa es Firebase, la plataforma de Google, '
        'en su plan Spark gratuito. Dentro de Firebase, los datos se gestionan con Cloud Firestore (base de datos NoSQL '
        'documental) y las cuentas con Firebase Authentication. El proyecto se creó como lumbre-hotel, con base de datos '
        '(default) en la ubicación nam5 (Estados Unidos), edición Standard y modo producción (todo cerrado por defecto).')
    d.h1('2. Justificación frente a cada requisito')
    d.table(['Requisito', 'Cómo lo cumple Firebase', 'Evidencia en el proyecto'], [
        ['R1 Costo cero', 'Plan Spark sin tarjeta.', 'Proyecto creado sin facturación.'],
        ['R2 Multiplataforma', 'API REST consumida con Ktor desde código común KMP.', 'FirestoreApi.kt y FirebaseAuthApi.kt en shared/.'],
        ['R3 Seguridad en servidor', 'Reglas declarativas evaluadas en cada operación con el token del usuario.', 'firebase/firestore.rules publicado.'],
        ['R4 Autenticación', 'Firebase Authentication: correo y contraseña, verificación y restablecimiento.', 'Pantalla de cuenta; contraseñas nunca llegan a la base de datos.'],
        ['R5 Tiempo real', 'Lecturas inmediatas; recepción refresca y ve reservas nuevas.', 'Pantalla de recepción.'],
        ['R6 Escalabilidad', 'Escalado automático gestionado por Google.', 'Sin servidores que administrar.'],
        ['R7 Operación simple', 'Consola con editor de datos, reglas y uso.', 'Rol de superusuario asignado desde la consola.'],
    ], [3.2, 6.3, 6.5], 'Cumplimiento de requisitos', 9)
    d.h1('3. Cómo se implementó')
    d.bullets([
        'Autenticación: endpoints accounts:signUp, signInWithPassword, sendOobCode, lookup, update y delete; renovación con securetoken (token de 1 h).',
        'Datos: documentos/colecciones con get, PATCH (crear/actualizar con máscara), DELETE, listado paginado y runQuery para "mis reservas".',
        'Codificación: un códec propio convierte tipos de Kotlin a valores tipados de Firestore (stringValue, integerValue, etc.).',
        'Repositorio: HotelRepository decide qué descargar según el rol y aplica actualizaciones optimistas con resincronización si el servidor rechaza.',
        'Modo local de respaldo: si Firebase no está configurado, la app funciona con almacenamiento del dispositivo.',
    ])
    d.h1('4. Del modelo relacional a colecciones')
    d.table(['Tabla (U4_6)', 'Colección / documento', 'Decisión'], [
        ['usuario + rol', 'users/{uid} (campo role)', 'El rol se guarda como texto en el usuario: lectura en una sola consulta para las reglas.'],
        ['tipo_habitacion', 'rooms/{STANDARD|DELUXE|PENTHOUSE}', 'Contenido editorial (fotos, amenidades) en la app; precio y disponibilidad en la nube.'],
        ['promocion', 'promos/{CODIGO}', 'La clave del documento es el código.'],
        ['reserva + reserva_extra', 'reservations/{LMB-XXXXXX}', 'Extras como arreglo dentro de la reserva (se leen siempre juntos).'],
        ['parametro', 'config/params', 'Un documento con todos los parámetros (una lectura).'],
        ['auditoria', 'audit/{autoId}', 'Solo alta; lectura del superusuario.'],
    ], [3.8, 4.8, 7.4], 'Mapeo relacional → Firestore', 9)
    d.h1('5. Reglas de seguridad en el servidor')
    d.code('''function level(role) { return role == 'SUPERADMIN' ? 3 : role == 'ADMIN' ? 2 : role == 'STAFF' ? 1 : 0; }
match /users/{uid} {
  allow create: if request.auth.uid == uid && request.resource.data.role == 'GUEST';
  allow update: if (request.auth.uid == uid && onlyChanges(['name','phone','lang','currency','theme','lastLogin']))
                || (isSuper() && request.auth.uid != uid && onlyChanges(['role','disabled']));
}
match /reservations/{ref} {
  allow read:   if resource.data.uid == request.auth.uid || isStaff();
  allow create: if request.resource.data.uid == request.auth.uid && request.resource.data.status == 'CONFIRMED'
                && request.resource.data.adults >= 1 && request.resource.data.adults <= 6
                && request.resource.data.checkOut > request.resource.data.checkIn;
}
match /audit/{id} { allow read: if isSuper(); allow create: if isStaff(); allow update, delete: if false; }''',
           'Extracto de firebase/firestore.rules (el archivo completo está en el repositorio).')
    d.h1('6. Límites del plan gratuito y uso previsto')
    d.table(['Recurso', 'Límite Spark', 'Uso estimado', 'Holgura'], [
        ['Almacenamiento', '1 GiB', '< 50 MB/año', '> 95 %'],
        ['Lecturas', '50 000/día', '≈ 3 000/día', '94 %'],
        ['Escrituras', '20 000/día', '≈ 400/día', '98 %'],
        ['Usuarios de Auth', 'Sin límite práctico (correo/contraseña)', '≈ 6 000/año', 'Amplia'],
    ], [3.5, 4.5, 4, 4], 'Capacidad')
    d.h1('7. Plan de migración')
    d.p('Si el hotel necesitara consultas analíticas complejas o integridad referencial estricta, el modelo relacional '
        'normalizado (U4_6) y su DDL para PostgreSQL permiten migrar a Supabase o a un PostgreSQL propio. En el código '
        'solo cambiaría la implementación del repositorio de datos; las pantallas no se tocan.')
    d.h1('8. Evidencia')
    d.bullets([f'Aplicación web: {APPWEB}', f'Repositorio: {REPO} (carpeta app/firebase y app/shared/.../data/firebase)',
               'Consola de Firebase: proyecto lumbre-hotel (acceso del propietario).'])
    d.h1('9. Modelo de datos NoSQL en Firebase')
    d.p('Firebase Cloud Firestore es una base de datos NoSQL documental: los datos se guardan en documentos (pares '
        'campo-valor) agrupados en colecciones, sin tablas ni JOIN. Este es el modelo real del proyecto:')
    d.diagram('11_modelo_nosql_firestore.png', 'Modelo NoSQL del proyecto en Firebase Cloud Firestore.', 16.5)
    d.diagram('12_relacional_vs_nosql.png', 'Transformación del modelo relacional al modelo documental.', 16.5)
    d.h1('10. Cómo protege Firebase cada operación')
    d.diagram('13_reglas_firebase.png', 'Evaluación de autenticación y reglas en cada escritura.', 12)
    d.h1('11. Acceso a datos desde la app')
    d.diagram('14_concurrencia.png', 'La app escribe en Firebase de forma asíncrona sin bloquear la interfaz.', 15)
    d.h1('12. Ventajas y desventajas de Firebase en este proyecto')
    d.pros_cons(['Costo cero hoy y al crecer moderadamente', 'Cuentas y seguridad listas sin programar un servidor',
                 'Mismo acceso desde Android, iOS y web', 'Cambios visibles en todos los dispositivos', 'Consola para revisar y corregir datos',
                 'Las reglas impiden que alguien se asigne un rol'],
                ['Sin JOIN: algunos datos se duplican (desnormalización)', 'Reportes complejos requieren exportar a otra herramienta',
                 'Depende de un proveedor (Google)', 'Sin respaldos automáticos en el plan gratuito: hay que exportar manualmente',
                 'Si el uso crece mucho, se paga por operación'], 'Firebase: ventajas y desventajas')
    d.tap(13, ['La UI refleja al instante cada cambio (actualización optimista).',
               'Todas las llamadas a Firebase son suspend y se ejecutan en un CoroutineScope propio.',
               'Firebase consulta, guarda y actualiza con reglas por rol en el servidor.',
               'El mismo acceso a datos funciona en Android, iOS y web.'])
    return d.save()


# ======================================================================================
# 6. DIAGRAMA RELACIONAL
# ======================================================================================
DDL = '''CREATE TABLE rol (
  id_rol      SMALLINT PRIMARY KEY,
  nombre      VARCHAR(20) NOT NULL UNIQUE,
  nivel       SMALLINT NOT NULL CHECK (nivel BETWEEN 0 AND 3)
);
CREATE TABLE usuario (
  id_usuario     VARCHAR(128) PRIMARY KEY,
  correo         VARCHAR(254) NOT NULL UNIQUE,
  nombre         VARCHAR(80)  NOT NULL CHECK (char_length(nombre) >= 2),
  telefono       VARCHAR(22),
  id_rol         SMALLINT NOT NULL DEFAULT 0 REFERENCES rol(id_rol),
  idioma         CHAR(2)  NOT NULL DEFAULT 'ES' CHECK (idioma IN ('ES','EN','PT','FR')),
  moneda         CHAR(3)  NOT NULL DEFAULT 'EUR' CHECK (moneda IN ('EUR','USD','MXN','GBP','BRL','COP')),
  tema           VARCHAR(6) NOT NULL DEFAULT 'LIGHT' CHECK (tema IN ('LIGHT','DARK','SYSTEM')),
  bloqueado      BOOLEAN NOT NULL DEFAULT FALSE,
  fecha_alta     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultimo_acceso  TIMESTAMP
);
CREATE TABLE tipo_habitacion (
  id_tipo           VARCHAR(12) PRIMARY KEY,
  nombre            VARCHAR(40) NOT NULL,
  descripcion       VARCHAR(200),
  superficie_m2     SMALLINT CHECK (superficie_m2 > 0),
  capacidad         SMALLINT NOT NULL CHECK (capacidad BETWEEN 1 AND 6),
  precio_noche_eur  NUMERIC(7,2) NOT NULL CHECK (precio_noche_eur BETWEEN 30 AND 5000),
  disponible        BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE amenidad (
  id_amenidad SMALLINT PRIMARY KEY,
  nombre      VARCHAR(40) NOT NULL UNIQUE
);
CREATE TABLE tipo_habitacion_amenidad (
  id_tipo     VARCHAR(12) REFERENCES tipo_habitacion(id_tipo) ON DELETE CASCADE,
  id_amenidad SMALLINT    REFERENCES amenidad(id_amenidad) ON DELETE CASCADE,
  PRIMARY KEY (id_tipo, id_amenidad)
);
CREATE TABLE promocion (
  codigo      VARCHAR(20) PRIMARY KEY CHECK (codigo ~ '^[A-Z0-9]{4,20}$'),
  porcentaje  SMALLINT NOT NULL CHECK (porcentaje BETWEEN 5 AND 50),
  activa      BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE reserva (
  referencia         CHAR(10) PRIMARY KEY CHECK (referencia ~ '^LMB-[A-Z2-9]{6}$'),
  id_usuario         VARCHAR(128) REFERENCES usuario(id_usuario) ON DELETE SET NULL,
  id_tipo            VARCHAR(12) NOT NULL REFERENCES tipo_habitacion(id_tipo),
  codigo_promocion   VARCHAR(20) REFERENCES promocion(codigo),
  nombre_huesped     VARCHAR(80)  NOT NULL,
  correo_contacto    VARCHAR(254) NOT NULL,
  telefono_contacto  VARCHAR(22),
  fecha_llegada      DATE NOT NULL,
  fecha_salida       DATE NOT NULL,
  adultos            SMALLINT NOT NULL CHECK (adultos BETWEEN 1 AND 6),
  ninos              SMALLINT NOT NULL DEFAULT 0 CHECK (ninos BETWEEN 0 AND 4),
  total_eur          NUMERIC(10,2) NOT NULL CHECK (total_eur > 0),
  estado             VARCHAR(12) NOT NULL DEFAULT 'CONFIRMED' CHECK (estado IN ('CONFIRMED','CHECKED_IN','CANCELLED')),
  notas              VARCHAR(500),
  fecha_creacion     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (fecha_salida > fecha_llegada),
  CHECK (fecha_salida - fecha_llegada <= 30)
);
CREATE TABLE extra (
  id_extra      VARCHAR(16) PRIMARY KEY,
  nombre        VARCHAR(40) NOT NULL,
  precio_eur    NUMERIC(6,2) NOT NULL CHECK (precio_eur >= 0),
  unidad_cobro  VARCHAR(20) NOT NULL CHECK (unidad_cobro IN ('PERSONA_NOCHE','ADULTO','ESTANCIA','NOCHE'))
);
CREATE TABLE reserva_extra (
  referencia   CHAR(10)    REFERENCES reserva(referencia) ON DELETE CASCADE,
  id_extra     VARCHAR(16) REFERENCES extra(id_extra),
  importe_eur  NUMERIC(8,2) NOT NULL CHECK (importe_eur >= 0),
  PRIMARY KEY (referencia, id_extra)
);
CREATE TABLE parametro (
  clave                VARCHAR(40) PRIMARY KEY,
  valor                VARCHAR(160) NOT NULL,
  descripcion          VARCHAR(200),
  id_usuario_modifica  VARCHAR(128) REFERENCES usuario(id_usuario) ON DELETE SET NULL,
  fecha_modificacion   TIMESTAMP
);
CREATE TABLE auditoria (
  id_auditoria  BIGSERIAL PRIMARY KEY,
  id_usuario    VARCHAR(128) NOT NULL REFERENCES usuario(id_usuario),
  fecha_hora    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  accion        VARCHAR(60) NOT NULL,
  objetivo      VARCHAR(120) NOT NULL
);
CREATE INDEX idx_reserva_usuario ON reserva(id_usuario);
CREATE INDEX idx_reserva_fechas  ON reserva(fecha_llegada, fecha_salida);
CREATE INDEX idx_auditoria_fecha ON auditoria(fecha_hora DESC);'''


def relacional():
    d = Doc('U4_BD/U4_6_Diagrama_Relacional.docx', U, 'Entregable U4_6 (Bases de datos)', 'Diagrama relacional normalizado',
            'Transformación del modelo E-R a tablas en 3FN con claves primarias, foráneas y restricciones')
    d.toc(['Reglas de transformación aplicadas', 'Diagrama relacional', 'Esquema relacional en notación textual',
           'Normalización paso a paso', 'Integridad referencial y acciones', 'Script DDL (PostgreSQL)',
           'Correspondencia con la implementación en Firestore', 'Del relacional al NoSQL de Firebase', 'Normalizado frente a desnormalizado', 'Criterios TAP'])
    d.h1('1. Reglas de transformación aplicadas')
    d.table(['Regla', 'Aplicación en el modelo'], [
        ['Cada entidad fuerte → tabla con su clave primaria', 'rol, usuario, tipo_habitacion, amenidad, promocion, reserva, extra, parametro, auditoria.'],
        ['Relación 1:N → clave foránea en el lado N', 'usuario.id_rol, reserva.id_usuario, reserva.id_tipo, reserva.codigo_promocion, auditoria.id_usuario, parametro.id_usuario_modifica.'],
        ['Relación N:M → tabla asociativa con PK compuesta', 'reserva_extra (referencia, id_extra) y tipo_habitacion_amenidad (id_tipo, id_amenidad).'],
        ['Participación opcional → FK que admite NULL', 'reserva.id_usuario y reserva.codigo_promocion.'],
        ['Atributo de la relación → columna de la tabla asociativa', 'reserva_extra.importe_eur.'],
        ['Dominios → tipos y CHECK', 'Rangos de adultos, niños, porcentaje, precio; listas de estados, idiomas y monedas.'],
    ], [6, 10], 'Reglas de transformación E-R → relacional')
    d.h1('2. Diagrama relacional')
    d.diagram('03_relacional.png', 'Diagrama relacional normalizado (PK, FK, UK, NN y CHECK indicados en cada columna).', 16.8)
    d.h1('3. Esquema relacional en notación textual')
    d.code('''ROL(id_rol PK, nombre UK, nivel)
USUARIO(id_usuario PK, correo UK, nombre, telefono, id_rol FK→ROL, idioma, moneda, tema, bloqueado, fecha_alta, ultimo_acceso)
TIPO_HABITACION(id_tipo PK, nombre, descripcion, superficie_m2, capacidad, precio_noche_eur, disponible)
AMENIDAD(id_amenidad PK, nombre UK)
TIPO_HABITACION_AMENIDAD(id_tipo PK FK→TIPO_HABITACION, id_amenidad PK FK→AMENIDAD)
PROMOCION(codigo PK, porcentaje, activa)
RESERVA(referencia PK, id_usuario FK→USUARIO NULL, id_tipo FK→TIPO_HABITACION, codigo_promocion FK→PROMOCION NULL,
        nombre_huesped, correo_contacto, telefono_contacto, fecha_llegada, fecha_salida, adultos, ninos,
        total_eur, estado, notas, fecha_creacion)
EXTRA(id_extra PK, nombre, precio_eur, unidad_cobro)
RESERVA_EXTRA(referencia PK FK→RESERVA, id_extra PK FK→EXTRA, importe_eur)
PARAMETRO(clave PK, valor, descripcion, id_usuario_modifica FK→USUARIO NULL, fecha_modificacion)
AUDITORIA(id_auditoria PK, id_usuario FK→USUARIO, fecha_hora, accion, objetivo)''')
    d.h1('4. Normalización paso a paso')
    d.h2('4.1 Punto de partida (no normalizado)')
    d.p('La hoja de cálculo original tenía una fila por reserva con columnas repetidas y valores compuestos, por ejemplo:')
    d.table(['referencia', 'huésped (rol)', 'habitación (capacidad, precio)', 'extras', 'promo (%)'], [
        ['LMB-H3XW9C', 'James Carter (GUEST)', 'Ático Lumbre (6, 340)', 'Desayuno, Spa, Traslado', 'LUMBRE10 (10)'],
    ], [3, 3.5, 4.5, 3.5, 2.5], 'Registro original (no normalizado)', 9)
    d.h2('4.2 Primera forma normal (1FN)')
    d.p('Se eliminan los grupos repetidos y valores multivaluados: la columna "extras" pasa a filas en RESERVA_EXTRA y las '
        'amenidades a TIPO_HABITACION_AMENIDAD. Todos los atributos quedan atómicos y cada tabla tiene clave primaria.')
    d.h2('4.3 Segunda forma normal (2FN)')
    d.p('En RESERVA_EXTRA (PK compuesta referencia + id_extra), el nombre y el precio de catálogo del extra dependen solo '
        'de id_extra (dependencia parcial). Se mueven a EXTRA; en RESERVA_EXTRA queda solo importe_eur, que depende de la '
        'clave completa (el importe cobrado en esa reserva).')
    d.h2('4.4 Tercera forma normal (3FN)')
    d.p('En RESERVA, la capacidad y el precio por noche dependen de id_tipo, no de la referencia (dependencia transitiva '
        'referencia → id_tipo → capacidad). Se trasladan a TIPO_HABITACION. Del mismo modo, el porcentaje depende del '
        'código (PROMOCION) y el nombre y nivel del rol dependen de id_rol (ROL).')
    d.h2('4.5 Comprobación de Boyce-Codd')
    d.p('En todas las tablas, cada determinante es clave candidata: correo es clave candidata en USUARIO (UNIQUE) y '
        'nombre en ROL y AMENIDAD (UNIQUE). No quedan dependencias en las que un atributo no clave determine otro.')
    d.table(['Tabla', 'Dependencias funcionales principales', 'Forma normal'], [
        ['usuario', 'id_usuario → correo, nombre, …, id_rol; correo → id_usuario', 'FNBC'],
        ['reserva', 'referencia → todos los atributos', 'FNBC'],
        ['reserva_extra', '(referencia, id_extra) → importe_eur', 'FNBC'],
        ['tipo_habitacion', 'id_tipo → nombre, capacidad, precio_noche_eur, …', 'FNBC'],
        ['promocion', 'codigo → porcentaje, activa', 'FNBC'],
    ], [3.5, 9.5, 3], 'Dependencias funcionales')
    d.note('Desnormalización controlada: total_eur se almacena (aunque se pueda calcular) para conservar el precio '
           'aceptado por el cliente aunque después cambien tarifas o parámetros; los datos de contacto de la reserva se '
           'conservan por el mismo motivo histórico.', 'Decisión justificada')
    d.h1('5. Integridad referencial y acciones')
    d.table(['FK', 'Referencia', 'Al borrar el padre'], [
        ['usuario.id_rol', 'rol', 'RESTRICT (no se borra un rol en uso)'],
        ['reserva.id_usuario', 'usuario', 'SET NULL (la reserva se conserva por obligación legal)'],
        ['reserva.id_tipo', 'tipo_habitacion', 'RESTRICT'],
        ['reserva.codigo_promocion', 'promocion', 'RESTRICT'],
        ['reserva_extra.referencia', 'reserva', 'CASCADE'],
        ['tipo_habitacion_amenidad.*', 'tipo_habitacion / amenidad', 'CASCADE'],
        ['auditoria.id_usuario', 'usuario', 'RESTRICT (la auditoría no se pierde)'],
    ], [5, 4.5, 6.5], 'Acciones referenciales')
    d.h1('6. Script DDL (PostgreSQL)')
    d.code(DDL, 'Script completo; también se guarda en docs/bd/lumbre.sql del repositorio.')
    d.h1('7. Correspondencia con la implementación en Firestore')
    d.p('El SMBD del proyecto es Firebase (ver U4_5): los datos viven en Cloud Firestore. Las mismas restricciones del DDL se aplican mediante '
        'reglas de seguridad (rangos, listas de valores, propietario de la reserva) y validaciones en la app. '
        'Las tablas asociativas se representan como arreglos dentro del documento padre porque siempre se leen juntas.')
    d.h1('8. Del modelo relacional al modelo NoSQL de Firebase')
    d.diagram('12_relacional_vs_nosql.png', 'Cómo se implementa este esquema relacional en Firebase.', 16.5)
    d.diagram('11_modelo_nosql_firestore.png', 'Resultado: colecciones y campos en Firestore.', 16.5)
    d.h1('9. Ventajas y desventajas: modelo normalizado frente a documento desnormalizado')
    d.h2('Modelo relacional normalizado (3FN)')
    d.pros_cons(['Sin datos repetidos', 'Integridad garantizada por el motor (FK, CHECK)', 'Consultas flexibles con JOIN'],
                ['Más tablas y uniones para leer una reserva completa', 'Requiere un servidor con API propia para la app'])
    d.h2('Documento desnormalizado en Firebase')
    d.pros_cons(['Una sola lectura trae la reserva completa', 'Más rápido en móvil con mala conexión', 'Encaja con las reglas por usuario'],
                ['Algunos datos se repiten (contacto, total)', 'La integridad depende de reglas y de la app'])
    d.tap(10, ['Las restricciones CHECK coinciden con las validaciones que ve el usuario.',
              'Las escrituras que respetan estas restricciones se hacen en segundo plano.',
              'El DDL documenta el acceso a datos y permite migrar a PostgreSQL.',
              'El modelo soporta las funciones móviles (mis reservas, recepción).'])
    return d.save()


# ======================================================================================
# 7. DICCIONARIO DE DATOS
# ======================================================================================
DICT = {
    'rol': ('Perfiles de permisos del sistema.', 'Firestore: campo users.role', [
        ('id_rol', 'Identificador del rol', 'SMALLINT', '2 bytes', 'NO', 'PK', '0 GUEST, 1 STAFF, 2 ADMIN, 3 SUPERADMIN', '—', '3'),
        ('nombre', 'Nombre del rol', 'VARCHAR', '20', 'NO', 'UK', 'Uno de GUEST, STAFF, ADMIN, SUPERADMIN', '—', 'SUPERADMIN'),
        ('nivel', 'Nivel jerárquico', 'SMALLINT', '2 bytes', 'NO', '', 'CHECK 0..3', '—', '3'),
    ]),
    'usuario': ('Personas con cuenta (huéspedes y personal).', 'Firestore: users/{uid}', [
        ('id_usuario', 'UID emitido por Firebase Authentication', 'VARCHAR', '128', 'NO', 'PK', 'Asignado por el proveedor', '—', 'kQ3…Zp2'),
        ('correo', 'Correo de acceso', 'VARCHAR', '254', 'NO', 'UK', 'Formato válido; igual al del token', '—', 'ana@correo.com'),
        ('nombre', 'Nombre y apellidos', 'VARCHAR', '80', 'NO', '', 'Mínimo 2, solo letras y ’ . -', '—', 'Ana Pérez'),
        ('telefono', 'Teléfono de contacto', 'VARCHAR', '22', 'SÍ', '', '7 a 15 dígitos; + ( ) . - permitidos', '—', '+52 55 1234 5678'),
        ('id_rol', 'Rol asignado', 'SMALLINT', '2 bytes', 'NO', 'FK', 'Al registrarse siempre 0 (GUEST)', 'rol.id_rol', '0'),
        ('idioma', 'Idioma preferido', 'CHAR', '2', 'NO', '', 'ES, EN, PT, FR', '—', 'ES'),
        ('moneda', 'Moneda preferida', 'CHAR', '3', 'NO', '', 'EUR, USD, MXN, GBP, BRL, COP', '—', 'MXN'),
        ('tema', 'Tema visual', 'VARCHAR', '6', 'NO', '', 'LIGHT, DARK, SYSTEM', '—', 'LIGHT'),
        ('bloqueado', 'Cuenta bloqueada', 'BOOLEAN', '1', 'NO', '', 'Solo el superusuario lo cambia', '—', 'false'),
        ('fecha_alta', 'Fecha de registro', 'TIMESTAMP', '8', 'NO', '', 'Automática', '—', '2026-11-18 21:05'),
        ('ultimo_acceso', 'Último inicio de sesión', 'TIMESTAMP', '8', 'SÍ', '', 'Se actualiza al entrar', '—', '2026-11-19 09:12'),
    ]),
    'tipo_habitacion': ('Categorías de habitación que se venden.', 'Firestore: rooms/{id}', [
        ('id_tipo', 'Identificador de la categoría', 'VARCHAR', '12', 'NO', 'PK', 'STANDARD, DELUXE, PENTHOUSE', '—', 'DELUXE'),
        ('nombre', 'Nombre comercial', 'VARCHAR', '40', 'NO', '', 'Traducido en la app', '—', 'Suite Deluxe Mar'),
        ('descripcion', 'Descripción breve', 'VARCHAR', '200', 'SÍ', '', '—', '—', 'Salón y balcón al mar'),
        ('superficie_m2', 'Superficie', 'SMALLINT', '2 bytes', 'SÍ', '', '> 0', '—', '42'),
        ('capacidad', 'Huéspedes máximos', 'SMALLINT', '2 bytes', 'NO', '', 'CHECK 1..6', '—', '3'),
        ('precio_noche_eur', 'Tarifa base por noche', 'NUMERIC', '7,2', 'NO', '', 'CHECK 30..5000', '—', '190.00'),
        ('disponible', 'Abierta a reserva', 'BOOLEAN', '1', 'NO', '', 'Editable por ADMIN', '—', 'true'),
    ]),
    'amenidad': ('Comodidades que ofrece cada tipo.', 'Contenido de la app (Catalog)', [
        ('id_amenidad', 'Identificador', 'SMALLINT', '2 bytes', 'NO', 'PK', '—', '—', '4'),
        ('nombre', 'Nombre', 'VARCHAR', '40', 'NO', 'UK', '—', '—', 'Bañera'),
    ]),
    'tipo_habitacion_amenidad': ('Relación N:M entre tipos y amenidades.', 'Contenido de la app (Catalog)', [
        ('id_tipo', 'Tipo de habitación', 'VARCHAR', '12', 'NO', 'PK, FK', 'CASCADE', 'tipo_habitacion.id_tipo', 'DELUXE'),
        ('id_amenidad', 'Amenidad', 'SMALLINT', '2 bytes', 'NO', 'PK, FK', 'CASCADE', 'amenidad.id_amenidad', '4'),
    ]),
    'promocion': ('Códigos de descuento.', 'Firestore: promos/{codigo}', [
        ('codigo', 'Código que escribe el cliente', 'VARCHAR', '20', 'NO', 'PK', '^[A-Z0-9]{4,20}$', '—', 'LUMBRE10'),
        ('porcentaje', 'Descuento', 'SMALLINT', '2 bytes', 'NO', '', 'CHECK 5..50', '—', '10'),
        ('activa', 'Vigente', 'BOOLEAN', '1', 'NO', '', '—', '—', 'true'),
    ]),
    'reserva': ('Estancias contratadas.', 'Firestore: reservations/{referencia}', [
        ('referencia', 'Identificador visible', 'CHAR', '10', 'NO', 'PK', '^LMB-[A-Z2-9]{6}$', '—', 'LMB-WPAEW3'),
        ('id_usuario', 'Dueño (si tenía cuenta)', 'VARCHAR', '128', 'SÍ', 'FK', 'SET NULL al borrar usuario', 'usuario.id_usuario', 'kQ3…Zp2'),
        ('id_tipo', 'Tipo reservado', 'VARCHAR', '12', 'NO', 'FK', 'Capacidad ≥ adultos + niños', 'tipo_habitacion.id_tipo', 'DELUXE'),
        ('codigo_promocion', 'Código aplicado', 'VARCHAR', '20', 'SÍ', 'FK', 'Debe estar activo al reservar', 'promocion.codigo', 'LUMBRE10'),
        ('nombre_huesped', 'Nombre del titular', 'VARCHAR', '80', 'NO', '', 'Validación de nombre', '—', 'Ana Pérez'),
        ('correo_contacto', 'Correo de contacto', 'VARCHAR', '254', 'NO', '', 'Formato válido', '—', 'ana@gmail.com'),
        ('telefono_contacto', 'Teléfono de contacto', 'VARCHAR', '22', 'SÍ', '', '7–15 dígitos', '—', '+52 55 1234 5678'),
        ('fecha_llegada', 'Check-in', 'DATE', '4', 'NO', '', '≥ hoy; ≤ hoy + 18 meses', '—', '2026-12-01'),
        ('fecha_salida', 'Check-out', 'DATE', '4', 'NO', '', '> llegada; ≤ 30 noches', '—', '2026-12-04'),
        ('adultos', 'Número de adultos', 'SMALLINT', '2 bytes', 'NO', '', 'CHECK 1..6', '—', '2'),
        ('ninos', 'Niños de 2 a 12 años', 'SMALLINT', '2 bytes', 'NO', '', 'CHECK 0..4', '—', '0'),
        ('total_eur', 'Total con impuestos', 'NUMERIC', '10,2', 'NO', '', '> 0; precio congelado', '—', '746.00'),
        ('estado', 'Situación', 'VARCHAR', '12', 'NO', '', 'CONFIRMED, CHECKED_IN, CANCELLED', '—', 'CONFIRMED'),
        ('notas', 'Peticiones especiales', 'VARCHAR', '500', 'SÍ', '', '—', '—', 'Cuna, por favor'),
        ('fecha_creacion', 'Momento de la reserva', 'TIMESTAMP', '8', 'NO', '', 'Automática', '—', '2026-11-18 20:41'),
    ]),
    'extra': ('Servicios adicionales.', 'Enumeración Extra en la app', [
        ('id_extra', 'Identificador', 'VARCHAR', '16', 'NO', 'PK', 'BREAKFAST, SPA, TRANSFER, PARKING, LATE_CHECKOUT', '—', 'BREAKFAST'),
        ('nombre', 'Nombre', 'VARCHAR', '40', 'NO', '', 'Traducido', '—', 'Desayuno buffet'),
        ('precio_eur', 'Precio de catálogo', 'NUMERIC', '6,2', 'NO', '', '≥ 0', '—', '18.00'),
        ('unidad_cobro', 'Base de cálculo', 'VARCHAR', '20', 'NO', '', 'PERSONA_NOCHE, ADULTO, ESTANCIA, NOCHE', '—', 'PERSONA_NOCHE'),
    ]),
    'reserva_extra': ('Extras incluidos en cada reserva.', 'Firestore: arreglo reservations.extras', [
        ('referencia', 'Reserva', 'CHAR', '10', 'NO', 'PK, FK', 'CASCADE', 'reserva.referencia', 'LMB-WPAEW3'),
        ('id_extra', 'Extra', 'VARCHAR', '16', 'NO', 'PK, FK', '—', 'extra.id_extra', 'BREAKFAST'),
        ('importe_eur', 'Importe cobrado', 'NUMERIC', '8,2', 'NO', '', '≥ 0', '—', '108.00'),
    ]),
    'parametro': ('Reglas configurables del negocio.', 'Firestore: config/params', [
        ('clave', 'Nombre del parámetro', 'VARCHAR', '40', 'NO', 'PK', 'taxPercent, maxNights, …', '—', 'taxPercent'),
        ('valor', 'Valor actual', 'VARCHAR', '160', 'NO', '', 'Rango validado por clave', '—', '10'),
        ('descripcion', 'Explicación', 'VARCHAR', '200', 'SÍ', '', '—', '—', 'Impuestos (%)'),
        ('id_usuario_modifica', 'Último en cambiarlo', 'VARCHAR', '128', 'SÍ', 'FK', 'Solo SUPERADMIN', 'usuario.id_usuario', 'kQ3…Zp2'),
        ('fecha_modificacion', 'Fecha del cambio', 'TIMESTAMP', '8', 'SÍ', '', '—', '—', '2026-11-18 21:30'),
    ]),
    'auditoria': ('Registro inmutable de acciones administrativas.', 'Firestore: audit/{autoId}', [
        ('id_auditoria', 'Identificador', 'BIGINT', '8', 'NO', 'PK', 'Autonumérico', '—', '1024'),
        ('id_usuario', 'Autor', 'VARCHAR', '128', 'NO', 'FK', 'Correo del token en Firestore', 'usuario.id_usuario', 'kQ3…Zp2'),
        ('fecha_hora', 'Momento', 'TIMESTAMP', '8', 'NO', '', 'Automático', '—', '2026-11-18 21:30'),
        ('accion', 'Tipo de acción', 'VARCHAR', '60', 'NO', '', 'ROOM_UPDATE, ROLE_CHANGE, …', '—', 'ROLE_CHANGE'),
        ('objetivo', 'Elemento afectado', 'VARCHAR', '120', 'NO', '', '—', '—', 'ana@correo.com → STAFF'),
    ]),
}

FS_DICT = [
    ('users/{uid}', 'Un documento por persona con cuenta. El id del documento es el UID de Firebase Authentication.', [
        ('name', 'string', 'Sí', 'Nombre y apellidos', 'App: 2–80 letras', 'Mariana López'),
        ('email', 'string', 'Sí', 'Correo de la cuenta', 'Regla: igual a request.auth.token.email al crear', 'mariana@correo.com'),
        ('phone', 'string', 'No', 'Teléfono de contacto', 'App: 7–15 dígitos', '+52 33 1234 5678'),
        ('role', 'string', 'Sí', 'Rol de permisos', 'Regla: GUEST al crear; solo SUPERADMIN lo cambia', 'GUEST'),
        ('disabled', 'boolean', 'Sí', 'Cuenta bloqueada', 'Regla: solo SUPERADMIN', 'false'),
        ('lang', 'string', 'Sí', 'Idioma preferido', 'Regla: ES|EN|PT|FR', 'ES'),
        ('currency', 'string', 'Sí', 'Moneda preferida', 'Regla: EUR|USD|MXN|GBP|BRL|COP', 'MXN'),
        ('theme', 'string', 'Sí', 'Tema visual', 'Regla: LIGHT|DARK|SYSTEM', 'LIGHT'),
        ('createdAt', 'integer', 'Sí', 'Alta (ms desde 1970)', '—', '1795061032319'),
        ('lastLogin', 'integer', 'No', 'Último acceso (ms)', 'Lo actualiza el propio usuario', '1795061064473'),
    ]),
    ('reservations/{ref}', 'Una reserva por documento; el id es la referencia visible.', [
        ('uid', 'string', 'Sí*', 'Dueño (UID); * en la nube siempre, en local puede faltar', 'Regla: == request.auth.uid al crear', 'kQ3…Zp2'),
        ('guestName', 'string', 'Sí', 'Titular', 'App: nombre válido', 'Mariana López'),
        ('email', 'string', 'Sí', 'Correo de contacto', 'App: formato válido', 'mariana@correo.com'),
        ('phone', 'string', 'No', 'Teléfono de contacto', 'App: 7–15 dígitos', '+52 33 1234 5678'),
        ('room', 'string', 'Sí', 'Tipo de habitación', 'Regla: STANDARD|DELUXE|PENTHOUSE', 'DELUXE'),
        ('checkIn', 'string', 'Sí', 'Fecha de llegada (ISO)', 'App: ≥ hoy, ≤ 18 meses', '2026-12-06'),
        ('checkOut', 'string', 'Sí', 'Fecha de salida (ISO)', 'Regla: checkOut > checkIn', '2026-12-09'),
        ('adults', 'integer', 'Sí', 'Adultos', 'Regla: 1..6', '2'),
        ('children', 'integer', 'Sí', 'Niños 2–12 años', 'Regla: 0..4', '0'),
        ('extras', 'array<string>', 'No', 'Extras contratados', 'Valores de Extra', '["BREAKFAST"]'),
        ('promo', 'string|null', 'No', 'Código aplicado', 'App: código activo', 'LUMBRE10'),
        ('totalEur', 'double', 'Sí', 'Total congelado en EUR', 'Regla: > 0', '746.0'),
        ('status', 'string', 'Sí', 'Estado', 'Regla: CONFIRMED al crear; dueño solo CANCELLED', 'CONFIRMED'),
        ('notes', 'string', 'No', 'Peticiones especiales', 'App: ≤ 500', 'Cuna, por favor'),
        ('createdAt', 'integer', 'Sí', 'Momento de la reserva (ms)', '—', '1795061100000'),
    ]),
    ('rooms/{roomId}', 'Datos editables de cada tipo de habitación (lo editorial vive en la app).', [
        ('nightlyEur', 'integer', 'Sí', 'Precio base por noche', 'Regla: 30..5000; solo ADMIN+', '190'),
        ('capacity', 'integer', 'Sí', 'Huéspedes máximos', 'Regla: 1..6', '3'),
        ('available', 'boolean', 'Sí', 'Abierta a reserva', 'Solo ADMIN+', 'true'),
    ]),
    ('promos/{code}', 'Códigos de descuento; el id es el código.', [
        ('percent', 'integer', 'Sí', 'Porcentaje de descuento', 'Regla: 5..50; id ^[A-Z0-9]{4,20}$', '10'),
        ('active', 'boolean', 'Sí', 'Vigente', 'Solo ADMIN+', 'true'),
    ]),
    ('config/params', 'Documento único con las reglas de negocio (ver tabla de parámetros).', [
        ('taxPercent … minPasswordLength', 'integer', 'Sí', '10 parámetros numéricos', 'Regla: rangos por campo; solo SUPERADMIN', '10, 15, 10, 7, 30, 18, 20, 5, 60, 8'),
        ('maintenance', 'boolean', 'Sí', 'Pausa reservas de huéspedes', 'Solo SUPERADMIN', 'false'),
        ('maintenanceMessage', 'string', 'No', 'Mensaje mostrado', '≤ 160', 'Volvemos a las 18:00'),
    ]),
    ('audit/{autoId}', 'Registro inmutable de acciones administrativas.', [
        ('at', 'integer', 'Sí', 'Momento (ms)', '—', '1795061200000'),
        ('actor', 'string', 'Sí', 'Correo del autor', 'Regla: == correo del token', 'recepcion@lumbre.com'),
        ('action', 'string', 'Sí', 'Tipo de acción', 'ROOM_UPDATE, ROLE_CHANGE, …', 'RES_STATUS'),
        ('target', 'string', 'Sí', 'Elemento afectado', '≤ 120 caracteres', 'LMB-7QK2PA → CHECKED_IN'),
    ]),
]

USO = {
    'rol': {
        'id_rol': 'Cuando el hotel decide qué puede hacer cada persona: el número indica el nivel de permisos.',
        'nombre': 'Aparece en el panel del superusuario junto a cada persona: Huésped, Recepción, Administrador o Superusuario.',
        'nivel': 'Cuando alguien abre una pestaña protegida: la app compara su nivel para mostrarla u ocultarla.',
    },
    'usuario': {
        'id_usuario': 'Cuando Mariana inicia sesión en otro celular: con este identificador la app encuentra su cuenta y sus reservas.',
        'correo': 'Cuando Mariana crea su cuenta o inicia sesión; también recibe ahí el enlace para recuperar su contraseña.',
        'nombre': 'Aparece en Perfil ("Hola, Mariana") y se rellena solo al reservar para no escribirlo otra vez.',
        'telefono': 'Lo usa recepción si necesita llamar a la persona (por ejemplo, si su vuelo se retrasa).',
        'id_rol': 'Cuando el superusuario convierte a una recepcionista en "Recepción": desde ese momento ve la pestaña de llegadas.',
        'idioma': 'Cuando Mariana cambia la app a inglés: al abrirla en la computadora ya aparece en inglés.',
        'moneda': 'Cuando eligió pesos: todos los precios se muestran en MXN en cualquier dispositivo.',
        'tema': 'Cuando prefiere el modo oscuro de noche: se conserva al volver a entrar.',
        'bloqueado': 'Cuando el hotel detecta un mal uso: el superusuario bloquea la cuenta y ya no puede entrar.',
        'fecha_alta': 'Permite saber desde cuándo es cliente (por ejemplo, para premiar a clientes frecuentes).',
        'ultimo_acceso': 'Ayuda al superusuario a ver qué cuentas siguen activas.',
    },
    'tipo_habitacion': {
        'id_tipo': 'Cuando Mariana elige "Suite Deluxe Mar" en el paso 2 de la reserva.',
        'nombre': 'Es el título que ve en la tarjeta de la habitación.',
        'descripcion': 'Es el texto corto que la convence: "Salón y balcón al mar".',
        'superficie_m2': 'Aparece como "42 m²" para comparar tamaños.',
        'capacidad': 'Cuando intenta reservar para 4 personas en una habitación de 3, la app le avisa que no caben.',
        'precio_noche_eur': 'Es la base de todo el presupuesto; si el administrador lo cambia, los nuevos presupuestos lo reflejan al instante.',
        'disponible': 'Si el hotel cierra una categoría por remodelación, deja de ofrecerse.',
    },
    'amenidad': {
        'id_amenidad': 'Identifica cada comodidad del catálogo.',
        'nombre': 'Aparece como etiqueta en el detalle: "Bañera", "Wi-Fi rápido", "Terraza".',
    },
    'tipo_habitacion_amenidad': {
        'id_tipo': 'Indica a qué habitación pertenece cada comodidad mostrada en su detalle.',
        'id_amenidad': 'Indica qué comodidad se muestra en esa habitación.',
    },
    'promocion': {
        'codigo': 'Cuando Mariana escribe LUMBRE10 o pulsa "Usar en mi reserva" en Ofertas.',
        'porcentaje': 'Es el descuento que aparece en verde en el presupuesto (−10 %).',
        'activa': 'Cuando termina la campaña, el administrador la desactiva y el código deja de funcionar.',
    },
    'reserva': {
        'referencia': 'Es el código que Mariana recibe (LMB-7MSZSJ) y que dicta en recepción al llegar.',
        'id_usuario': 'Hace que la reserva aparezca en "Mis reservas" en todos sus dispositivos.',
        'id_tipo': 'Indica qué habitación reservó; aparece en la tarjeta de la reserva.',
        'codigo_promocion': 'Deja constancia del descuento que se aplicó.',
        'nombre_huesped': 'Recepción lo ve en "Llegadas de hoy" para recibir a la persona por su nombre.',
        'correo_contacto': 'Para enviar confirmaciones o avisos sobre la estancia.',
        'telefono_contacto': 'Para contactar a la persona si hay un imprevisto.',
        'fecha_llegada': 'Decide en qué día aparece en "Llegadas de hoy" de recepción.',
        'fecha_salida': 'Decide cuándo aparece en "Salidas de hoy" y cuándo pasa a "Pasadas".',
        'adultos': 'Calcula el precio de extras por persona y comprueba que quepan en la habitación.',
        'ninos': 'Los niños pagan la mitad del desayuno; también cuentan para la capacidad.',
        'total_eur': 'Es el precio que se respetará aunque el hotel suba tarifas después.',
        'estado': 'Muestra "Confirmada", "En el hotel" o "Cancelada" en la tarjeta y en recepción.',
        'notas': 'Recepción lee peticiones como "Cuna, por favor" antes de que llegue el huésped.',
        'fecha_creacion': 'Ordena las reservas de la más nueva a la más antigua en el panel.',
    },
    'extra': {
        'id_extra': 'Cuando Mariana marca "Desayuno buffet" en el paso 2.',
        'nombre': 'Es el texto del botón del extra.',
        'precio_eur': 'Se suma al presupuesto en cuanto se marca el extra.',
        'unidad_cobro': 'Decide si se cobra por persona y noche, por adulto o una sola vez.',
    },
    'reserva_extra': {
        'referencia': 'Une cada extra con la reserva de Mariana.',
        'id_extra': 'Indica qué extra contrató.',
        'importe_eur': 'Guarda lo que pagó por ese extra, aunque el precio cambie después.',
    },
    'parametro': {
        'clave': 'Identifica la regla que se está cambiando (por ejemplo, impuestos).',
        'valor': 'Cuando el superusuario sube el recargo de fin de semana a 20 %, todos los presupuestos nuevos lo usan sin actualizar la app.',
        'descripcion': 'Explica al superusuario para qué sirve cada parámetro.',
        'id_usuario_modifica': 'Permite saber quién cambió la regla.',
        'fecha_modificacion': 'Permite saber cuándo se cambió.',
    },
    'auditoria': {
        'id_auditoria': 'Identifica cada registro del historial.',
        'id_usuario': 'Dice quién hizo el cambio (por ejemplo, la recepcionista del turno de noche).',
        'fecha_hora': 'Dice cuándo ocurrió.',
        'accion': 'Dice qué se hizo: cambio de precio, de rol, registro de llegada…',
        'objetivo': 'Dice a qué se le hizo: "LMB-7QK2PA → En el hotel".',
    },
}


def diccionario():
    d = Doc('U4_BD/U4_7_Diccionario_de_Datos.docx', U, 'Entregable U4_7 (Bases de datos)', 'Diccionario de datos',
            'Cada tabla y campo con descripción, tipo, tamaño, restricciones, relación, ejemplo y uso en la plataforma')
    d.toc(['Convenciones', 'Resumen de tablas'] + [f'Tabla {t}' for t in DICT] + ['Parámetros del sistema', 'Dominios y listas de valores', 'Diccionario NoSQL de Firebase', 'Criterios TAP'])
    d.h1('1. Convenciones')
    d.table(['Abreviatura', 'Significado'], [
        ['PK', 'Clave primaria'], ['FK', 'Clave foránea'], ['UK', 'Valor único'], ['NULO = NO', 'Campo obligatorio'],
        ['CHECK', 'Restricción de dominio'], ['Tamaño', 'Longitud máxima o precisión,escala'],
    ], [4, 12], 'Convenciones')
    d.h1('2. Resumen de tablas')
    d.table(['Tabla', 'Descripción', 'Implementación', 'Campos'],
            [[k, v[0], v[1], str(len(v[2]))] for k, v in DICT.items()], [3.8, 6, 4.8, 1.4], 'Tablas del modelo', 9)
    n = 3
    for name, (desc, impl, cols) in DICT.items():
        d.h1(f'{n}. Tabla {name}')
        d.p(desc, bold_prefix='Descripción:')
        d.p(impl, bold_prefix='Implementación actual:')
        d.table(['Campo', 'Descripción', 'Tipo', 'Tamaño', 'Nulo', 'Clave', 'Restricciones', 'Relación', 'Ejemplo'],
                [list(c) for c in cols], [2.4, 2.6, 1.6, 1.2, 0.9, 1.1, 2.9, 2.3, 2.0], f'Diccionario de {name}', 7.5)
        if name in USO:
            d.table(['Campo', 'Cuándo se usa en la plataforma (ejemplo cotidiano)'],
                    [[c[0], USO[name].get(c[0], '—')] for c in cols], [3.4, 12.6], f'Uso de {name} en la plataforma', 9)
        n += 1
    d.h1(f'{n}. Parámetros del sistema')
    d.p('Cada parámetro lo cambia el superusuario desde la web y se nota de inmediato en la app, sin publicar una nueva versión.')
    d.table(['Clave', 'Descripción', 'Valor por defecto', 'Rango válido'], [
        ['taxPercent', 'Impuestos sobre el total', '10', '0–30'],
        ['weekendSurchargePercent', 'Recargo por noche de viernes y sábado', '15', '0–50'],
        ['longStayDiscountPercent', 'Descuento por larga estancia', '10', '0–50'],
        ['longStayNights', 'Noches para aplicar el descuento', '7', '2–30'],
        ['maxNights', 'Noches máximas por reserva', '30', '1–90'],
        ['maxMonthsAhead', 'Antelación máxima', '18', '1–24'],
        ['bookingCooldownSec', 'Espera entre reservas (anti-abuso)', '20', '0–600'],
        ['maxLoginAttempts', 'Intentos fallidos antes de bloquear', '5', '3–10'],
        ['lockoutSec', 'Duración del bloqueo', '60', '30–3600'],
        ['minPasswordLength', 'Longitud mínima de contraseña', '8', '8–64'],
        ['maintenance', 'Pausa las reservas de huéspedes', 'false', 'true/false'],
        ['maintenanceMessage', 'Mensaje mostrado', '(vacío)', '≤ 160 caracteres'],
    ], [4.2, 6.3, 2.8, 2.7], 'Parámetros (tabla parametro / documento config/params)', 9)
    n += 1
    d.h1(f'{n}. Dominios y listas de valores')
    d.table(['Dominio', 'Valores'], [
        ['Estado de reserva', 'CONFIRMED (confirmada), CHECKED_IN (en el hotel), CANCELLED (cancelada)'],
        ['Rol', 'GUEST, STAFF, ADMIN, SUPERADMIN'],
        ['Idioma', 'ES, EN, PT, FR'],
        ['Moneda', 'EUR, USD, MXN, GBP, BRL, COP (tipo de cambio aproximado, base EUR)'],
        ['Tema', 'LIGHT, DARK, SYSTEM'],
        ['Unidad de cobro de extra', 'PERSONA_NOCHE (niños al 50 %), ADULTO, ESTANCIA, NOCHE'],
    ], [4.5, 11.5], 'Dominios')
    n += 1
    d.h1(f'{n}. Diccionario del modelo NoSQL en Firebase (implementación real)')
    d.p('Diccionario de las colecciones tal como existen en Firebase Cloud Firestore. "Regla" indica la validación que '
        'aplica el servidor (firestore.rules); "App" la que aplica la interfaz.')
    for col, desc, campos in FS_DICT:
        d.h2(col)
        d.p(desc)
        d.table(['Campo', 'Tipo Firestore', 'Obligatorio', 'Descripción', 'Regla / validación', 'Ejemplo'],
                [list(c) for c in campos], [2.4, 2.1, 1.5, 3.7, 3.7, 2.6], f'Diccionario de {col}', 8)
    d.diagram('11_modelo_nosql_firestore.png', 'Modelo NoSQL documentado en este diccionario.', 16)
    n += 1
    d.tap(n, ['Cada campo indica el mensaje de validación que ve el usuario.',
              'Los campos de fecha en milisegundos permiten ordenar eventos asíncronos.',
              'Documenta exactamente qué se consulta y guarda en cada colección.',
              'Incluye los datos que usa la app móvil (reservas, perfil, preferencias).'])
    return d.save()


ALL = [contexto, diagrama_contexto, diagrama_er, criterios, eleccion, relacional, diccionario]
