"""Presentación del proyecto (16:9) en .pptx; se sube a Drive como Presentaciones de Google."""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Cm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DIAG = os.path.join(ROOT, 'docs', 'diagramas')
SHOT = os.path.join(ROOT, 'docs', 'capturas')
OUT = os.path.join(ROOT, 'docs', 'entregables', 'Presentacion_Proyecto_Lumbre.pptx')

TEAL, NAVY, SUN, SAND, WHITE, GREY = (RGBColor(0x0A, 0x7C, 0x86), RGBColor(0x16, 0x31, 0x3A), RGBColor(0xF4, 0xA6, 0x3A),
                                      RGBColor(0xFF, 0xF4, 0xE2), RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0x5B, 0x6E, 0x73))
SERIF, SANS = 'Playfair Display', 'Inter'
W, H = Cm(33.867), Cm(19.05)

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]


def rect(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    r = s.shapes.add_shape(shape, x, y, w, h)
    r.fill.solid(); r.fill.fore_color.rgb = color; r.line.fill.background()
    return r


def text(s, x, y, w, h, t, size=18, color=NAVY, bold=False, font=SANS, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    lines = t if isinstance(t, list) else [t]
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
        p.space_after = Pt(6)
    return tb


def bullets(s, x, y, w, h, items, size=16, color=NAVY):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(9)
        head, _, rest = it.partition('|')
        r = p.add_run(); r.text = '●  '; r.font.color.rgb = SUN; r.font.size = Pt(size - 4); r.font.name = SANS
        if rest:
            r = p.add_run(); r.text = head.strip() + ' '; r.font.bold = True; r.font.size = Pt(size); r.font.color.rgb = TEAL; r.font.name = SANS
            r = p.add_run(); r.text = rest.strip(); r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = SANS
        else:
            r = p.add_run(); r.text = head.strip(); r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = SANS
    return tb


def pic(s, path, x, y, w, h, border=False):
    """Inserta la imagen ajustada dentro de la caja (x, y, w, h) conservando proporción y centrada."""
    if not os.path.exists(path):
        return
    iw, ih = Image.open(path).size
    k = min(w / iw, h / ih)
    pw, ph = int(iw * k), int(ih * k)
    px, py = x + (w - pw) // 2, y + (h - ph) // 2
    if border:
        rect(s, px - Cm(0.15), py - Cm(0.15), pw + Cm(0.3), ph + Cm(0.3), RGBColor(0xE6, 0xF6, 0xFA), MSO_SHAPE.ROUNDED_RECTANGLE)
    s.shapes.add_picture(path, px, py, pw, ph)


def slide(title, kicker, ref=None):
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, W, H, WHITE)
    rect(s, 0, 0, Cm(0.6), H, TEAL)
    text(s, Cm(1.6), Cm(0.8), Cm(28), Cm(1), kicker.upper(), 12, SUN, True)
    text(s, Cm(1.6), Cm(1.5), Cm(30), Cm(2), title, 30, NAVY, True, SERIF)
    if ref:
        tag = rect(s, W - Cm(9.2), Cm(0.8), Cm(8.2), Cm(1.0), SAND, MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = tag.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        r = tf.paragraphs[0].add_run(); r.text = ref; r.font.size = Pt(11); r.font.color.rgb = NAVY; r.font.name = SANS; r.font.bold = True
    text(s, Cm(1.6), H - Cm(1.1), Cm(30), Cm(0.8), 'Lumbre Hotel & Spa · Kotlin Multiplatform + Firebase', 10, GREY)
    return s


# 1 · Portada ------------------------------------------------------------------------
s = prs.slides.add_slide(BLANK)
pic(s, os.path.join(SHOT, 'escritorio_inicio_cookies.jpg'), 0, 0, W, H)
ov = rect(s, 0, 0, W, H, NAVY); ov.fill.transparency = 0.25
from pptx.oxml.ns import qn
sf = ov.fill._xPr.find(qn('a:solidFill'))
alpha = sf[0].makeelement(qn('a:alpha'), {'val': '72000'}); sf[0].append(alpha)
text(s, Cm(2), Cm(4.5), Cm(30), Cm(1.2), 'TECNM · INSTITUTO TECNOLÓGICO DE MORELIA', 14, SUN, True)
text(s, Cm(2), Cm(5.6), Cm(30), Cm(3), 'Lumbre Hotel & Spa', 54, WHITE, True, SERIF)
text(s, Cm(2), Cm(8.6), Cm(28), Cm(2), 'Sistema de reservas multiplataforma: Android · iOS · Web', 22, WHITE)
text(s, Cm(2), Cm(11.2), Cm(28), Cm(3), ['Unidad 1 · Interfaz centrada en el usuario', 'Unidad 2 · Librerías y componentes · Bases de datos',
                                          'Criterios TAP · Unidades 3 y 5'], 16, WHITE)
text(s, Cm(2), Cm(16.2), Cm(30), Cm(1), 'Jan Carlo Prado Anguiano · Noviembre de 2026', 14, SUN, True)

# 2 · Oportunidad --------------------------------------------------------------------
s = slide('Una oportunidad, no un problema', '1 · Contexto', 'U1 §1 · U2_1 Contexto')
bullets(s, Cm(1.6), Cm(4), Cm(16), Cm(13), [
    'Hoy|reservas por teléfono, correo y hojas de cálculo: duplicados y errores de captura.',
    'Huéspedes de 8 países|necesitan su idioma y su moneda.',
    'La oportunidad|una app que presupuesta, valida y confirma en menos de 1 minuto.',
    'Cómo la llevamos a cabo|usuario → UX → UI → desarrollo KMP → pruebas → mejoras.',
    'Costo|0 € de operación (Firebase Spark + GitHub Pages).'])
pic(s, os.path.join(DIAG, '01_contexto.png'), Cm(18), Cm(3.6), Cm(15), Cm(14), True)

# 3 · Usuario --------------------------------------------------------------------------
s = slide('Conoce a Mariana, 34 años', '2 · Usuario objetivo', 'U1 §2–4 · User Persona')
bullets(s, Cm(1.6), Cm(4), Cm(18), Cm(13), [
    'Perfil|arquitecta en Guadalajara, viaja 2–3 veces al año; experiencia tecnológica media.',
    'Necesita|precio total en pesos antes de dar sus datos; reservar desde el celular.',
    'Objetivo|reservar 3 noches frente al mar en menos de 5 minutos.',
    'Frustraciones|formularios largos, "Dato incorrecto", costos ocultos.',
    'Secundarios|recepción (llegadas del día) y administración (precios).'])
pic(s, os.path.join(SHOT, 'movil_reserva_paso1.jpg'), Cm(21), Cm(3.4), Cm(5.8), Cm(14.6), True)
pic(s, os.path.join(SHOT, 'movil_confirmacion.jpg'), Cm(27.2), Cm(3.4), Cm(5.8), Cm(14.6), True)

# 4 · Solución -----------------------------------------------------------------------
s = slide('Una app, tres plataformas', '3 · La solución', 'U2_E3 · Aplicación')
pic(s, os.path.join(SHOT, 'web_05_reserva_presupuesto.jpg'), Cm(1.6), Cm(4), Cm(19), Cm(12), True)
pic(s, os.path.join(SHOT, 'movil_01_inicio.jpg'), Cm(21.5), Cm(3.6), Cm(5.4), Cm(13.6), True)
pic(s, os.path.join(SHOT, 'movil_mis_reservas.jpg'), Cm(27.4), Cm(3.6), Cm(5.4), Cm(13.6), True)
text(s, Cm(1.6), Cm(16.4), Cm(19), Cm(1.2), 'Un solo código Kotlin: 14 pantallas · 4 idiomas · 6 monedas · web, Android e iOS', 14, TEAL, True)

# 5 · UX ------------------------------------------------------------------------------
s = slide('De la visita a la confirmación', '4 · User Flow y prototipo', 'U1 §6–7 · U1_E3 Prototipo')
pic(s, os.path.join(DIAG, '15_user_flow.png'), Cm(1.6), Cm(3.6), Cm(9.5), Cm(14.4), True)
pic(s, os.path.join(DIAG, '18_wireframes_todos.png'), Cm(12), Cm(3.6), Cm(21), Cm(14.4), True)

# 6 · Principios UX --------------------------------------------------------------------
s = slide('Principios UX aplicados', '5 · Experiencia de usuario', 'U1 §5 · 7 principios')
bullets(s, Cm(1.6), Cm(4), Cm(15), Cm(14), [
    'Retroalimentación|presupuesto en vivo, confeti y referencia.',
    'Prevención de errores|validación junto al campo y sugerencias.',
    'Consistencia|mismos colores y botones en web y móvil.',
    'Navegación clara|pasos, Atrás y X siempre visibles.',
    'Reconocimiento|Lumi y textos guían sin memorizar.',
    'Jerarquía visual|un botón principal por pantalla.',
    'Accesibilidad|tema claro/oscuro, contraste, 4 idiomas.'], 15)
pic(s, os.path.join(SHOT, 'movil_reserva_paso3.jpg'), Cm(17.5), Cm(3.4), Cm(5), Cm(14.6), True)
pic(s, os.path.join(SHOT, 'movil_cancelar_dialogo.jpg'), Cm(22.9), Cm(3.4), Cm(5), Cm(14.6), True)
pic(s, os.path.join(SHOT, 'movil_02_preferencias_capacidades.jpg'), Cm(28.3), Cm(3.4), Cm(5), Cm(14.6), True)

# 7 · Validaciones ---------------------------------------------------------------------
s = slide('Validaciones que explican qué hacer', '6 · Validación y retroalimentación', 'U1 §12–13 · U2_E1 §8')
pic(s, os.path.join(SHOT, 'web_07_validaciones.jpg'), Cm(1.6), Cm(3.8), Cm(19), Cm(12.5), True)
bullets(s, Cm(21.5), Cm(4), Cm(11.5), Cm(14), [
    '10 validaciones|nombre, correo, teléfono, fechas, cantidades, contraseña, código, consentimiento.',
    'Mensajes claros|"La salida debe ser posterior a la llegada."',
    'Sugerencias|"¿Quisiste decir ana@gmail.com?"',
    'Doble capa|la app valida y Firebase vuelve a validar en el servidor.'], 14)

# 8 · Arquitectura ------------------------------------------------------------------
s = slide('Arquitectura por módulos', '7 · Librerías y componentes', 'U2_E2 · gitdiagram.com')
pic(s, os.path.join(DIAG, '19_arquitectura_modulos.png'), Cm(1.6), Cm(3.6), Cm(22), Cm(14.4), True)
bullets(s, Cm(24.4), Cm(4), Cm(9), Cm(14), [
    'Compose Multiplatform|UI', 'Navigation|rutas tipadas', 'Ktor|HTTP', 'Firebase|Auth + Firestore',
    'kotlinx|datetime · serialization', 'settings|almacenamiento local', '15 componentes propios|documentados'], 13)

# 9 · Concurrencia ----------------------------------------------------------------------
s = slide('Síncrono y asíncrono sin bloquear', '8 · Criterio TAP: componentes síncronos y asíncronos', 'U2_E2 §9')
pic(s, os.path.join(DIAG, '14_concurrencia.png'), Cm(1.6), Cm(3.6), Cm(20.5), Cm(14.4), True)
bullets(s, Cm(22.8), Cm(4), Cm(10.4), Cm(14), [
    'Síncrono|validación y presupuesto al instante.',
    'Asíncrono|34 funciones suspend con Ktor.',
    'CoroutineScope|SupervisorJob + Dispatchers.Default.',
    'Reactivo|StateFlow → la UI se recompone sola.',
    'Errores|SharedFlow → Snackbar y resincronización.'], 13)

# 10 · Firebase NoSQL ------------------------------------------------------------------
s = slide('Firebase: base de datos NoSQL', '9 · Elección del SMBD', 'U2_5 Elección · U2_7 Diccionario')
pic(s, os.path.join(DIAG, '11_modelo_nosql_firestore.png'), Cm(1.6), Cm(3.6), Cm(20), Cm(14.4), True)
bullets(s, Cm(22.4), Cm(4), Cm(10.8), Cm(14), [
    'Matriz ponderada|Firebase 4.80 / PostgreSQL 4.40.',
    'Colecciones|users · reservations · rooms · promos · config · audit.',
    'Desnormalización|extras embebidos y total congelado.',
    'Plan Spark|0 € · 50 000 lecturas/día.'], 13)

# 11 · Modelo de datos --------------------------------------------------------------
s = slide('Del contexto al modelo relacional', '10 · Bases de datos', 'U2_2 · U2_3 · U2_6')
pic(s, os.path.join(DIAG, '01b_dfd_nivel1.png'), Cm(1.6), Cm(3.6), Cm(15.5), Cm(7), True)
pic(s, os.path.join(DIAG, '02a_er_chen.png'), Cm(1.6), Cm(11), Cm(15.5), Cm(7), True)
pic(s, os.path.join(DIAG, '03_relacional.png'), Cm(17.6), Cm(3.6), Cm(15.6), Cm(14.4), True)

# 12 · Seguridad ----------------------------------------------------------------------
s = slide('Seguridad y privacidad', '11 · Acceso a datos seguro', 'U2_E1 §9 · U2_5 §5')
pic(s, os.path.join(DIAG, '13_reglas_firebase.png'), Cm(1.6), Cm(3.6), Cm(11), Cm(14.4), True)
pic(s, os.path.join(SHOT, 'escritorio_super_seguridad.jpg'), Cm(13.2), Cm(3.8), Cm(12.5), Cm(7.5), True)
pic(s, os.path.join(SHOT, 'movil_cookies.jpg'), Cm(26.4), Cm(3.6), Cm(6.8), Cm(14.4), True)
bullets(s, Cm(13.2), Cm(11.8), Cm(12.6), Cm(6), [
    'Reglas por rol|en el servidor.', 'Bloqueo|tras 5 intentos.', 'Ubicación|solo con permiso, ~11 km.'], 13)

# 13 · Roles y paneles -----------------------------------------------------------------
s = slide('Móvil útil, web completa', '12 · Roles y paneles', 'U2_E1 §4 · U2_E3 §6')
pic(s, os.path.join(SHOT, 'escritorio_admin_panel.jpg'), Cm(1.6), Cm(3.8), Cm(15.6), Cm(9.4), True)
pic(s, os.path.join(SHOT, 'escritorio_super_parametros.jpg'), Cm(17.6), Cm(3.8), Cm(15.6), Cm(9.4), True)
bullets(s, Cm(1.6), Cm(13.8), Cm(31), Cm(4), [
    'GUEST → STAFF → ADMIN → SUPERADMIN|cada rol ve solo sus pestañas; el superusuario cambia roles y parámetros sin publicar versión.',
    'Móvil|reservar, mis reservas, llave digital y recepción.', 'Web|todo, incluidos los paneles de administración y superusuario.'], 13)

# 14 · Componentes externos -------------------------------------------------------------
s = slide('Componentes externos: una oportunidad', '13 · Integración y reutilización', 'U2_E4 · U2_E5')
bullets(s, Cm(1.6), Cm(4), Cm(16), Cm(14), [
    '10 componentes de la web|Compose, Ktor, Firebase, Unsplash, Google Fonts, PlantUML…',
    'Sin SDK de Firebase para Wasm|→ REST con Ktor y códec propio.',
    'Pruebas no corrían en Node|→ pruebas en la JVM.',
    'Reutilización|100 % del código en 3 plataformas.',
    'Feedback|7 observaciones reales atendidas.'], 14)
pic(s, os.path.join(DIAG, '09_dependencias_externas.png'), Cm(18), Cm(3.6), Cm(15.2), Cm(14.4), True)

# 15 · Resultados y criterios --------------------------------------------------------------
s = slide('Resultados y criterios de evaluación', '14 · Resultados', 'Matriz TAP en cada entregable')
rows = [('Interfaz gráfica', '14 pantallas, retroalimentación inmediata, diseño adaptable'),
        ('Componentes síncronos/asíncronos', 'Corrutinas, Flows y Ktor; la UI nunca se bloquea'),
        ('Acceso a datos', 'Firebase con reglas por rol, sincronización y copia local'),
        ('Propuesta móvil', 'Oportunidad, persona, funciones y KMP Android/iOS')]
tbl = s.shapes.add_table(len(rows) + 1, 2, Cm(1.6), Cm(4), Cm(20), Cm(9)).table
tbl.columns[0].width = Cm(7); tbl.columns[1].width = Cm(13)
for j, h in enumerate(('Criterio (25 % c/u)', 'Evidencia')):
    c = tbl.cell(0, j); c.text = h
    c.fill.solid(); c.fill.fore_color.rgb = TEAL
    r = c.text_frame.paragraphs[0].runs[0]; r.font.color.rgb = WHITE; r.font.bold = True; r.font.size = Pt(14); r.font.name = SANS
for i, (a, b) in enumerate(rows, 1):
    for j, v in enumerate((a, b)):
        c = tbl.cell(i, j); c.text = v
        c.fill.solid(); c.fill.fore_color.rgb = SAND if i % 2 else WHITE
        r = c.text_frame.paragraphs[0].runs[0]; r.font.size = Pt(13); r.font.color.rgb = NAVY; r.font.name = SANS; r.font.bold = (j == 0)
bullets(s, Cm(22.6), Cm(4), Cm(10.6), Cm(14), [
    '14 pruebas|en verde.', '16 documentos|+ video de 3:07.', 'Reserva|en menos de 1 minuto.', '0 €|de operación.'], 15)
pic(s, os.path.join(SHOT, 'escritorio_recepcion.jpg'), Cm(1.6), Cm(13.4), Cm(20), Cm(4.6))

# 16 · Cierre ----------------------------------------------------------------------------
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
text(s, Cm(2), Cm(3), Cm(30), Cm(2.5), '¡Gracias!', 54, WHITE, True, SERIF)
bullets(s, Cm(2), Cm(6.5), Cm(20), Cm(8), [
    'Aprendimos|que una interfaz es buena cuando el usuario se recupera solo de sus errores.',
    'La seguridad|vive en el servidor; el cliente solo mejora la experiencia.',
    'Siguiente paso|pagos de prueba, notificaciones y pruebas de UI automatizadas.'], 16, WHITE)
text(s, Cm(2), Cm(14.5), Cm(30), Cm(3), ['App web: jancarliux24.github.io/hotel-lumbre/app', 'Código: github.com/JanCarliux24/hotel-lumbre',
                                          'APK: jancarliux24.github.io/hotel-lumbre/app/lumbre.apk'], 14, SUN, True)
pic(s, os.path.join(SHOT, 'movil_confirmacion.jpg'), Cm(24.5), Cm(2), Cm(7.5), Cm(15.5), True)

prs.save(OUT)
print(OUT, len(prs.slides), 'diapositivas')
