"""Entregables de la Unidad 4 — Bases de datos (7 documentos)."""
from docgen import Doc, WEB, APPWEB, REPO

U = 'Unidad 4 · Bases de datos'


# ======================================================================================
# 1. CONTEXTO
# ======================================================================================
def contexto():
    d = Doc('BD1_Contexto.docx', U, 'Entregable BD 1', 'Contexto del problema y propósito de la base de datos',
            'Por qué Lumbre necesita una base de datos y a qué necesidades del sistema responde')
    d.toc(['Resumen', 'Descripción de la organización', 'Problema actual', 'Propósito de la base de datos',
           'Contexto de uso: quién, dónde y cuándo', 'Necesidades del sistema y datos que las satisfacen',
           'Requisitos de datos', 'Volumen y crecimiento estimado', 'Restricciones y supuestos',
           'Indicadores de éxito', 'Relación con los demás entregables'])

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
    d.p('Con este volumen la base de datos cabe holgadamente en el plan gratuito elegido (ver Entregable BD 5): '
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
    d.p('Este contexto se representa gráficamente en el diagrama de contexto (BD 2), se modela en el diagrama '
        'entidad-relación (BD 3), justifica los criterios y la elección del sistema gestor (BD 4 y BD 5), se transforma '
        'en el diagrama relacional normalizado (BD 6) y se documenta campo a campo en el diccionario de datos (BD 7).')
    d.p(f'Aplicación funcionando: {APPWEB} · Código: {REPO}')
    return d.save()


# ======================================================================================
# 2. DIAGRAMA DE CONTEXTO
# ======================================================================================
def diagrama_contexto():
    d = Doc('BD2_Diagrama_de_Contexto.docx', U, 'Entregable BD 2', 'Diagrama de contexto',
            'El sistema, sus actores externos y los flujos de información que intercambian')
    d.toc(['Objetivo del diagrama', 'Diagrama de contexto (nivel 0)', 'Simbología utilizada', 'Actores externos',
           'Flujos de información', 'Límites del sistema', 'Reglas de lectura y coherencia', 'Supuestos'])
    d.h1('1. Objetivo del diagrama')
    d.p('El diagrama de contexto (Diagrama de Flujo de Datos de nivel 0) muestra el sistema completo como un único '
        'proceso y lo rodea de todas las entidades externas con las que intercambia información. Sirve para delimitar '
        'el alcance: todo lo que está dentro del círculo es responsabilidad del sistema y su base de datos; todo lo de '
        'fuera son personas o servicios con los que se comunica.')
    d.h1('2. Diagrama de contexto (nivel 0)')
    d.diagram('01_contexto.png', 'Diagrama de contexto de Lumbre Hotel & Spa (DFD nivel 0, notación Yourdon/DeMarco).')
    d.h1('3. Simbología utilizada')
    d.table(['Símbolo', 'Significado', 'En este diagrama'], [
        ['Óvalo (proceso 0)', 'El sistema completo como una caja negra.', 'Sistema de reservas Lumbre (app Android, iOS y web + base de datos).'],
        ['Rectángulo crema', 'Entidad externa humana (actor).', 'Huésped, Recepción, Administrador, Superusuario.'],
        ['Rectángulo azul', 'Sistema o servicio externo.', 'Firebase Authentication, Cloud Firestore, geolocalización, correo.'],
        ['Flecha con etiqueta', 'Flujo de datos y su sentido.', 'Qué información viaja y hacia dónde.'],
    ], [3.5, 5.5, 7], 'Simbología')
    d.h1('4. Actores externos')
    d.table(['Actor', 'Tipo', 'Rol en el sistema'], [
        ['Huésped', 'Persona', 'Explora, presupuesta, reserva, consulta y cancela; usa la llave digital en móvil.'],
        ['Recepción (STAFF)', 'Persona', 'Registra llegadas y cambia estados de reserva (móvil y web).'],
        ['Administrador (ADMIN)', 'Persona', 'Gestiona precios, disponibilidad y promociones (web).'],
        ['Superusuario (SUPERADMIN)', 'Persona', 'Gestiona usuarios, roles, parámetros, auditoría (web).'],
        ['Firebase Authentication', 'Servicio', 'Autentica y emite tokens de sesión; gestiona contraseñas.'],
        ['Cloud Firestore', 'Servicio', 'Almacena los datos y aplica reglas de seguridad.'],
        ['Geolocalización (BigDataCloud)', 'Servicio', 'Convierte coordenadas aproximadas en código de país.'],
        ['Correo de Firebase', 'Servicio', 'Envía verificación de correo y restablecimiento de contraseña.'],
    ], [4.5, 2.5, 9], 'Actores externos')
    d.h1('5. Flujos de información')
    d.table(['#', 'Origen → destino', 'Flujo de datos', 'Descripción'], [
        ['F1', 'Huésped → Sistema', 'Datos de reserva', 'Fechas, huéspedes, habitación, extras, código promocional, nombre, correo, teléfono.'],
        ['F2', 'Huésped → Sistema', 'Consentimiento', 'Elección de cookies (necesarias, preferencias, ubicación).'],
        ['F3', 'Sistema → Huésped', 'Presupuesto y confirmación', 'Desglose con impuestos, referencia LMB-XXXXXX, mis reservas, llave digital.'],
        ['F4', 'Recepción → Sistema', 'Cambios de estado', 'Registro de llegada, cancelación.'],
        ['F5', 'Sistema → Recepción', 'Listas del día', 'Llegadas, huéspedes en el hotel y salidas.'],
        ['F6', 'Administrador → Sistema', 'Catálogo', 'Precio por noche, disponibilidad, promociones.'],
        ['F7', 'Sistema → Administrador', 'Indicadores', 'Reservas activas, ingresos, ocupación, ticket medio.'],
        ['F8', 'Superusuario → Sistema', 'Gobierno', 'Roles, bloqueo de cuentas, parámetros del sistema.'],
        ['F9', 'Sistema → Superusuario', 'Supervisión', 'Lista de usuarios, auditoría, estado de seguridad.'],
        ['F10', 'Sistema ↔ Firebase Auth', 'Credenciales / token', 'Alta, inicio de sesión, renovación; devuelve UID y token de 1 h.'],
        ['F11', 'Sistema ↔ Firestore', 'Documentos', 'Lectura/escritura autorizada por reglas según el rol.'],
        ['F12', 'Sistema ↔ Geolocalización', 'País', 'Envía coordenadas redondeadas a ~11 km; recibe el código de país.'],
        ['F13', 'Auth → Correo → Huésped', 'Mensajes', 'Verificación de correo y restablecimiento de contraseña.'],
    ], [1, 4, 3.5, 7.5], 'Flujos de información del diagrama', 9)
    d.h1('6. Límites del sistema')
    d.bullets([
        'Dentro: interfaz de las tres plataformas, reglas de negocio (presupuesto y validaciones), sincronización y base de datos.',
        'Fuera: identidad (Firebase Authentication), envío de correos, servicio de geocodificación inversa.',
        'No incluido en esta versión: pagos en línea, asignación de número físico de habitación, facturación electrónica.',
    ])
    d.h1('7. Reglas de lectura y coherencia')
    d.bullets([
        'Cada flecha tiene un nombre que describe el dato, no la acción.',
        'Ningún flujo conecta dos entidades externas sin pasar por el sistema, salvo el correo, que lo origina el servicio de autenticación (se muestra porque llega al huésped).',
        'Los mismos actores y servicios aparecen en el diagrama E-R y en el diccionario de datos con los mismos nombres.',
        'Cada flujo de entrada tiene al menos un flujo de salida que da respuesta al actor.',
    ])
    d.h1('8. Supuestos')
    d.bullets(['El personal usa cuentas individuales; no hay cuentas compartidas.',
               'Los servicios externos usados son gratuitos y no requieren tarjeta.'])
    return d.save()


# ======================================================================================
# 3. DIAGRAMA ENTIDAD-RELACIÓN
# ======================================================================================
def diagrama_er():
    d = Doc('BD3_Diagrama_Entidad_Relacion.docx', U, 'Entregable BD 3', 'Diagrama entidad-relación',
            'Entidades, atributos, claves, relaciones y cardinalidades del problema')
    d.toc(['Método seguido', 'Diagrama E-R', 'Entidades y atributos', 'Relaciones y cardinalidades',
           'Reglas de negocio que justifican las cardinalidades', 'Resolución de relaciones N:M',
           'Atributos calculados y derivados', 'Validación del modelo con casos reales'])
    d.h1('1. Método seguido')
    d.bullets([
        'Se extrajeron sustantivos del contexto (BD 1) y de los casos de uso: usuario, rol, habitación, reserva, extra, promoción, parámetro, auditoría, amenidad.',
        'Se descartaron conceptos que son atributos (idioma, moneda, estado) o que no se almacenan (ubicación exacta).',
        'Se identificó la clave primaria de cada entidad priorizando identificadores naturales estables (código de promoción, referencia de reserva).',
        'Se definieron relaciones con su cardinalidad mínima y máxima a partir de reglas de negocio verificables.',
        'Se validó el modelo recorriendo escenarios reales (sección 8).',
    ], numbered=True)
    d.h1('2. Diagrama E-R')
    d.diagram('02_entidad_relacion.png', 'Modelo entidad-relación conceptual (notación pata de gallo).', 13.5)
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
    d.p('Las dos relaciones N:M se transforman en el modelo relacional (BD 6) en tablas asociativas: RESERVA_EXTRA '
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
    return d.save()


# ======================================================================================
# 4. CRITERIOS DE SELECCIÓN
# ======================================================================================
CANDIDATOS = ['Firebase (Cloud Firestore + Authentication)', 'PostgreSQL (Supabase)', 'MySQL 8 (autoalojado)', 'SQL Server Express', 'MongoDB Atlas', 'SQLite']


def criterios():
    d = Doc('BD4_Criterios_de_Seleccion_SMBD.docx', U, 'Entregable BD 4', 'Criterios de selección de un SMBD',
            'Análisis técnico, económico, de seguridad, escalabilidad, compatibilidad y facilidad de uso')
    d.toc(['Requisitos que condicionan la elección', 'Criterios y su peso', 'Candidatos evaluados',
           'Análisis por criterio', 'Matriz de decisión ponderada', 'Riesgos y mitigaciones', 'Conclusión'])
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
        ['Dependencia de proveedor', 'Modelo relacional documentado (BD 6) y DDL listo para PostgreSQL; repositorio de datos aislado en el código.'],
    ], [6, 10], 'Riesgos')
    d.h1('7. Conclusión')
    d.p('Los criterios técnicos, económicos, de seguridad, escalabilidad, compatibilidad y facilidad de uso apuntan a '
        'un SMBD gestionado con seguridad declarativa en servidor y acceso REST multiplataforma. Por eso el SMBD '
        'seleccionado es Firebase (Cloud Firestore + Authentication); la justificación detallada está en el Entregable BD 5.')
    return d.save()


# ======================================================================================
# 5. ELECCIÓN
# ======================================================================================
def eleccion():
    d = Doc('BD5_Eleccion_del_SMBD.docx', U, 'Entregable BD 5', 'Elección del SMBD: Firebase',
            'Por qué Firebase (Cloud Firestore + Authentication) es el SMBD del proyecto y cómo se implementó')
    d.toc(['Decisión', 'Justificación frente a cada requisito', 'Cómo se implementó', 'Del modelo relacional a colecciones',
           'Reglas de seguridad en el servidor', 'Límites del plan gratuito y uso previsto', 'Plan de migración', 'Evidencia'])
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
    d.table(['Tabla (BD 6)', 'Colección / documento', 'Decisión'], [
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
        'normalizado (BD 6) y su DDL para PostgreSQL permiten migrar a Supabase o a un PostgreSQL propio. En el código '
        'solo cambiaría la implementación del repositorio de datos; las pantallas no se tocan.')
    d.h1('8. Evidencia')
    d.bullets([f'Aplicación web: {APPWEB}', f'Repositorio: {REPO} (carpeta app/firebase y app/shared/.../data/firebase)',
               'Consola de Firebase: proyecto lumbre-hotel (acceso del propietario).'])
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
    d = Doc('BD6_Diagrama_Relacional.docx', U, 'Entregable BD 6', 'Diagrama relacional normalizado',
            'Transformación del modelo E-R a tablas en 3FN con claves primarias, foráneas y restricciones')
    d.toc(['Reglas de transformación aplicadas', 'Diagrama relacional', 'Esquema relacional en notación textual',
           'Normalización paso a paso', 'Integridad referencial y acciones', 'Script DDL (PostgreSQL)',
           'Correspondencia con la implementación en Firestore'])
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
    d.p('El SMBD del proyecto es Firebase (ver BD 5): los datos viven en Cloud Firestore. Las mismas restricciones del DDL se aplican mediante '
        'reglas de seguridad (rangos, listas de valores, propietario de la reserva) y validaciones en la app. '
        'Las tablas asociativas se representan como arreglos dentro del documento padre porque siempre se leen juntas.')
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


def diccionario():
    d = Doc('BD7_Diccionario_de_Datos.docx', U, 'Entregable BD 7', 'Diccionario de datos',
            'Cada tabla y campo con descripción, tipo, tamaño, restricciones y relación')
    d.toc(['Convenciones', 'Resumen de tablas'] + [f'Tabla {t}' for t in DICT] + ['Parámetros del sistema', 'Dominios y listas de valores'])
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
        n += 1
    d.h1(f'{n}. Parámetros del sistema')
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
    return d.save()


ALL = [contexto, diagrama_contexto, diagrama_er, criterios, eleccion, relacional, diccionario]
