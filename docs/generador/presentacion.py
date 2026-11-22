"""Presentación del proyecto (16:9). Se sube a Drive como Presentaciones de Google."""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DIAG = os.path.join(ROOT, 'docs', 'diagramas')
SHOT = os.path.join(ROOT, 'docs', 'capturas')
OUT = os.path.join(ROOT, 'docs', 'entregables', 'Presentacion_Proyecto_Lumbre.pptx')

TEAL, NAVY, SUN, SAND, WHITE, GREY = (RGBColor(0x0A, 0x7C, 0x86), RGBColor(0x16, 0x31, 0x3A), RGBColor(0xF4, 0xA6, 0x3A),
                                      RGBColor(0xFF, 0xF4, 0xE2), RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0x5B, 0x6E, 0x73))
MINT, PAPER, LINE = RGBColor(0xE6, 0xF6, 0xFA), RGBColor(0xF7, 0xFA, 0xFA), RGBColor(0xDC, 0xE8, 0xEA)
GREEN, RED, GOLD = RGBColor(0x20, 0x7A, 0x4F), RGBColor(0xB3, 0x26, 0x1E), RGBColor(0xB8, 0x7A, 0x1E)
SERIF, SANS = 'Playfair Display', 'Inter'
W, H = Cm(33.867), Cm(19.05)
VISOR = 'jancarliux24.github.io/hotel-lumbre/diagramas'

prs = Presentation()
prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]
TOTAL = 25
num = [0]


def rect(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE, line=None):
    r = s.shapes.add_shape(shape, x, y, w, h)
    r.fill.solid(); r.fill.fore_color.rgb = color
    if line is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = line; r.line.width = Pt(1)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        r.adjustments[0] = 0.08
    r.shadow.inherit = False
    return r


def alpha(shape, val):
    sf = shape.fill._xPr.find(qn('a:solidFill'))
    sf[0].append(sf[0].makeelement(qn('a:alpha'), {'val': str(val)}))


def text(s, x, y, w, h, t, size=18, color=NAVY, bold=False, font=SANS, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=6):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Cm(0.1)
    for i, ln in enumerate(t if isinstance(t, list) else [t]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(spacing)
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    return tb


def bullets(s, x, y, w, h, items, size=16, color=NAVY, gap=9, head_color=None):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        head, _, rest = it.partition('|')
        r = p.add_run(); r.text = '●  '; r.font.color.rgb = SUN; r.font.size = Pt(size - 4); r.font.name = SANS
        if rest:
            r = p.add_run(); r.text = head.strip() + '  '; r.font.bold = True; r.font.size = Pt(size); r.font.color.rgb = head_color or TEAL; r.font.name = SANS
            r = p.add_run(); r.text = rest.strip(); r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = SANS
        else:
            r = p.add_run(); r.text = head.strip(); r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = SANS
    return tb


def pic(s, path, x, y, w, h, frame=True, pad=Cm(0.25)):
    """Imagen ajustada a la caja conservando proporción; opcionalmente sobre una tarjeta blanca con borde."""
    if not os.path.exists(path):
        return
    iw, ih = Image.open(path).size
    k = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    pw, ph = int(iw * k), int(ih * k)
    px, py = x + (w - pw) // 2, y + (h - ph) // 2
    if frame:
        rect(s, px - pad, py - pad, pw + 2 * pad, ph + 2 * pad, WHITE, MSO_SHAPE.ROUNDED_RECTANGLE, LINE)
    s.shapes.add_picture(path, px, py, pw, ph)


def cover(s, path, x, y, w, h):
    """Imagen que cubre toda la caja (recorte centrado), para fondos."""
    iw, ih = Image.open(path).size
    k = max(w / iw, h / ih)
    pw, ph = int(iw * k), int(ih * k)
    p = s.shapes.add_picture(path, x + (w - pw) // 2, y + (h - ph) // 2, pw, ph)
    # recorte para no salirse de la diapositiva
    cl = max(0, (pw - w) / 2 / pw); ct = max(0, (ph - h) / 2 / ph)
    p.crop_left = p.crop_right = cl; p.crop_top = p.crop_bottom = ct
    p.left, p.top, p.width, p.height = x, y, w, h


def caption(s, x, y, w, t):
    text(s, x, y, w, Cm(0.8), t, 11, GREY, False, SANS, PP_ALIGN.CENTER)


def chip(s, x, y, w, t, fill=SAND, color=NAVY, size=11):
    c = rect(s, x, y, w, Cm(0.9), fill, MSO_SHAPE.ROUNDED_RECTANGLE)
    c.adjustments[0] = 0.5
    tf = c.text_frame; tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t; r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = SANS; r.font.bold = True
    return c


def footer(s, light=False):
    c = WHITE if light else GREY
    if not light:
        text(s, Cm(1.5), H - Cm(1.0), Cm(20), Cm(0.7), 'Lumbre Hotel & Spa · Kotlin Multiplatform + Firebase', 9, GREY)
        rect(s, Cm(22), H - Cm(0.72), Cm(8.5), Cm(0.12), LINE)
        rect(s, Cm(22), H - Cm(0.72), int(Cm(8.5) * num[0] / TOTAL), Cm(0.12), TEAL)
    text(s, Cm(30.8), H - Cm(1.0), Cm(2.4), Cm(0.7), f'{num[0]} / {TOTAL}', 10, c, True, SANS, PP_ALIGN.RIGHT)


def slide(title, kicker, ref=None):
    num[0] += 1
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, W, H, WHITE)
    rect(s, 0, 0, Cm(0.5), H, TEAL)
    text(s, Cm(1.5), Cm(0.75), Cm(24), Cm(0.8), kicker.upper(), 11, SUN, True)
    text(s, Cm(1.5), Cm(1.35), Cm(24.5), Cm(2), title, 28, NAVY, True, SERIF)
    if ref:
        chip(s, W - Cm(8.4), Cm(0.9), Cm(7.4), ref)
    footer(s)
    return s


def divider(n, title, sub, img):
    num[0] += 1
    s = prs.slides.add_slide(BLANK)
    cover(s, os.path.join(SHOT, img), 0, 0, W, H)
    ov = rect(s, 0, 0, W, H, NAVY); alpha(ov, 91000)
    rect(s, Cm(2.2), Cm(6.4), Cm(0.25), Cm(6.0), SUN)
    text(s, Cm(3), Cm(6.2), Cm(20), Cm(1.4), n, 20, SUN, True)
    text(s, Cm(3), Cm(7.5), Cm(30), Cm(3), title, 38, WHITE, True, SERIF)
    text(s, Cm(3), Cm(10.9), Cm(28), Cm(2), sub, 18, WHITE)
    footer(s, True)
    return s


def card(s, x, y, w, h, title, items, fill=PAPER, title_color=TEAL, size=13):
    rect(s, x, y, w, h, fill, MSO_SHAPE.ROUNDED_RECTANGLE, LINE)
    text(s, x + Cm(0.5), y + Cm(0.35), w - Cm(1), Cm(1), title, 15, title_color, True)
    bullets(s, x + Cm(0.5), y + Cm(1.35), w - Cm(1), h - Cm(1.6), items, size, NAVY, 5)


def table(s, x, y, w, rows, widths, size=12, head=TEAL):
    t = s.shapes.add_table(len(rows), len(rows[0]), x, y, w, Cm(0.9) * len(rows)).table
    for j, cw in enumerate(widths):
        t.columns[j].width = Cm(cw)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.text = v
            c.margin_left = c.margin_right = Cm(0.2); c.margin_top = c.margin_bottom = Cm(0.08)
            c.fill.solid(); c.fill.fore_color.rgb = head if i == 0 else (PAPER if i % 2 else WHITE)
            for p in c.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(size); r.font.name = SANS
                    r.font.color.rgb = WHITE if i == 0 else NAVY; r.font.bold = (i == 0 or j == 0)
    return t


# =========================================================================================== 1 · portada
num[0] += 1
s = prs.slides.add_slide(BLANK)
cover(s, os.path.join(SHOT, 'escritorio_inicio_cookies.jpg'), 0, 0, W, H)
ov = rect(s, 0, 0, W, H, NAVY); alpha(ov, 90000)
rect(s, Cm(2), Cm(4.2), Cm(0.25), Cm(8.6), SUN)
text(s, Cm(2.8), Cm(4.0), Cm(28), Cm(1), 'TECNM · INSTITUTO TECNOLÓGICO DE MORELIA', 13, SUN, True)
text(s, Cm(2.8), Cm(5.0), Cm(28), Cm(3), 'Lumbre Hotel & Spa', 56, WHITE, True, SERIF)
text(s, Cm(2.8), Cm(8.2), Cm(26), Cm(1.4), 'Sistema de reservas multiplataforma · Android · iOS · Web', 20, WHITE)
for i, t in enumerate(['Unidad 1 · Interfaz', 'Unidad 2 · Librerías', 'Unidad 4 · Bases de datos', 'Unidades 3 y 5 · Móvil']):
    chip(s, Cm(2.8) + Cm(6.6) * i, Cm(10.3), Cm(6.2), t)
text(s, Cm(2.8), Cm(15.6), Cm(28), Cm(1), 'Jan Carlo Prado Anguiano · Noviembre de 2026', 14, WHITE, True)

# =========================================================================================== 2 · agenda
s = slide('Agenda', 'Recorrido de la presentación')
secs = [('01', 'La oportunidad y el usuario', 'Por qué existe Lumbre y para quién'),
        ('02', 'Unidad 1 · Interfaz', 'User flow, prototipo, UX y validaciones'),
        ('03', 'Unidad 2 · Librerías', 'Arquitectura, síncrono/asíncrono, componentes'),
        ('04', 'Unidad 4 · Bases de datos', 'Contexto, DFD, E-R, modelo y Firebase'),
        ('05', 'Móvil y web', 'Qué tiene cada plataforma y por qué'),
        ('06', 'Resultados', 'Costos, resultados y conclusiones')]
for i, (n, t, d) in enumerate(secs):
    col, row = i % 3, i // 3
    x, y = Cm(1.5) + Cm(10.5) * col, Cm(4.2) + Cm(6.2) * row
    rect(s, x, y, Cm(10), Cm(5.6), PAPER, MSO_SHAPE.ROUNDED_RECTANGLE, LINE)
    text(s, x + Cm(0.6), y + Cm(0.5), Cm(4), Cm(1.6), n, 36, SUN, True, SERIF)
    text(s, x + Cm(0.6), y + Cm(2.3), Cm(9), Cm(1.2), t, 17, NAVY, True)
    text(s, x + Cm(0.6), y + Cm(3.5), Cm(9), Cm(1.6), d, 13, GREY)

# =========================================================================================== 3 · oportunidad
s = slide('Una oportunidad, no un problema', '01 · Contexto', 'U1 §1 · U4_1')
card(s, Cm(1.5), Cm(4), Cm(10), Cm(13.2), 'Hoy', ['Reservas por teléfono, correo y hojas de cálculo', 'Duplicados y errores de captura',
                                                  'El precio final se conoce al final', 'Clientes de 8 países, un solo idioma'], PAPER, RED, 17)
card(s, Cm(12), Cm(4), Cm(10), Cm(13.2), 'La oportunidad', ['Presupuesto exacto en segundos', 'Reserva en menos de 1 minuto',
                                                            'Idioma y moneda de cada país', 'Mismas reservas en cualquier dispositivo'], MINT, TEAL, 17)
card(s, Cm(22.5), Cm(4), Cm(10), Cm(13.2), 'Cómo la llevamos a cabo', ['Usuario → necesidades', 'UX → prototipo → UI', 'Kotlin Multiplatform + Firebase',
                                                                       'Pruebas y mejoras en ciclos', '0 € de operación'], SAND, GOLD, 17)

# =========================================================================================== 4 · usuario
s = slide('Conoce a Mariana', '01 · Usuario objetivo', 'U1 §2–4')
rect(s, Cm(1.5), Cm(4), Cm(19), Cm(13.2), PAPER, MSO_SHAPE.ROUNDED_RECTANGLE, LINE)
c = rect(s, Cm(2.3), Cm(4.8), Cm(3), Cm(3), TEAL, MSO_SHAPE.OVAL)
tf = c.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = 'M'; r.font.size = Pt(40); r.font.color.rgb = WHITE; r.font.name = SERIF; r.font.bold = True
text(s, Cm(6), Cm(4.9), Cm(14), Cm(1.4), 'Mariana López, 34 años', 22, NAVY, True, SERIF)
text(s, Cm(6), Cm(6.3), Cm(14), Cm(1.2), 'Arquitecta en Guadalajara · persona ficticia', 13, GREY)
bullets(s, Cm(2.3), Cm(8.6), Cm(17.5), Cm(8.5), ['Experiencia|media: usa banca móvil y compras en línea',
                                                    'Necesita|ver el total en pesos antes de dar sus datos',
                                                    'Objetivo|reservar 3 noches frente al mar en < 5 min',
                                                    'Frustración|formularios largos y "Dato incorrecto"'], 14)
text(s, Cm(2.3), Cm(14.6), Cm(17.5), Cm(2), '“Si no veo el precio final rápido, cierro la página.”', 17, TEAL, False, SERIF)
pic(s, os.path.join(SHOT, 'movil_reserva_paso1.jpg'), Cm(21.3), Cm(3.8), Cm(5.6), Cm(13.6))
pic(s, os.path.join(SHOT, 'movil_confirmacion.jpg'), Cm(27.3), Cm(3.8), Cm(5.6), Cm(13.6))

# =========================================================================================== 5 · solución
s = slide('Una app, tres plataformas', '01 · La solución', 'U2_E3')
pic(s, os.path.join(SHOT, 'web_05_reserva_presupuesto.jpg'), Cm(1.5), Cm(3.9), Cm(19.5), Cm(12.4))
caption(s, Cm(1.5), Cm(16.4), Cm(19.5), 'Web: reserva con presupuesto siempre visible')
pic(s, os.path.join(SHOT, 'movil_01_inicio.jpg'), Cm(21.5), Cm(3.7), Cm(5.5), Cm(12.7))
pic(s, os.path.join(SHOT, 'movil_mis_reservas.jpg'), Cm(27.4), Cm(3.7), Cm(5.5), Cm(12.7))
caption(s, Cm(21.5), Cm(16.4), Cm(11.4), 'Teléfono: inicio y mis reservas')

# =========================================================================================== 6 · divisor U1
divider('02', 'Unidad 1 · Interfaz centrada en el usuario', 'User flow, prototipo, principios UX, validaciones y retroalimentación', 'web_03_habitaciones.jpg')

# =========================================================================================== 7 · flujo y prototipo
s = slide('De la visita a la confirmación', '02 · User flow y prototipo', 'U1 §6–7 · U1_E3')
pic(s, os.path.join(DIAG, '15_user_flow.png'), Cm(1.5), Cm(3.8), Cm(9.6), Cm(13.6))
pic(s, os.path.join(DIAG, '18_wireframes_todos.png'), Cm(11.6), Cm(3.8), Cm(21.3), Cm(13.6))

# =========================================================================================== 8 · principios UX
s = slide('Por qué es fácil de usar', '02 · Principios UX', 'U1 §5')
pr = [('Retroalimentación', 'presupuesto en vivo y confirmación'), ('Prevención de errores', 'validación junto al campo'),
      ('Consistencia', 'mismo estilo en web y móvil'), ('Navegación clara', 'pasos, Atrás y X visibles'),
      ('Reconocimiento', 'Lumi guía cada paso'), ('Jerarquía visual', 'un botón principal'), ('Accesibilidad', 'contraste, temas, 4 idiomas')]
for i, (t, d) in enumerate(pr):
    y = Cm(3.9) + Cm(1.9) * i
    rect(s, Cm(1.5), y, Cm(15), Cm(1.6), PAPER if i % 2 else MINT, MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, Cm(2), y + Cm(0.3), Cm(6), Cm(1), t, 14, TEAL, True)
    text(s, Cm(8), y + Cm(0.32), Cm(8.4), Cm(1), d, 13, NAVY)
for j, (f, c_) in enumerate((('movil_reserva_paso3.jpg', 'Prevención'), ('movil_cancelar_dialogo.jpg', 'Confirmar antes de cancelar'),
                             ('movil_confirmacion.jpg', 'Retroalimentación'))):
    pic(s, os.path.join(SHOT, f), Cm(17.2) + Cm(5.3) * j, Cm(3.8), Cm(5.1), Cm(12.4))
    caption(s, Cm(17.2) + Cm(5.3) * j, Cm(16.3), Cm(5.1), c_)

# =========================================================================================== 9 · validaciones
s = slide('Validaciones que explican qué hacer', '02 · Validación y retroalimentación', 'U1 §12–13')
pic(s, os.path.join(SHOT, 'web_07_validaciones.jpg'), Cm(1.5), Cm(3.8), Cm(19.5), Cm(12.6))
bullets(s, Cm(21.8), Cm(4.1), Cm(11), Cm(13), ['10 validaciones|nombre, correo, teléfono, fechas, cantidades, contraseña, código y consentimiento',
                                                 'Mensajes claros|"La salida debe ser posterior a la llegada."',
                                                 'Sugerencias|"¿Quisiste decir ana@gmail.com?"',
                                                 'Doble capa|la app valida y Firebase vuelve a validar'], 14)

# =========================================================================================== 10 · divisor U2
divider('03', 'Unidad 2 · Librerías y componentes', 'Cómo está construida por dentro y qué piezas de terceros usamos', 'escritorio_admin_catalogo.jpg')

# =========================================================================================== 11 · arquitectura
s = slide('Cómo está organizada por dentro', '03 · Arquitectura por módulos', 'U2_E2 · gitdiagram.com')
pic(s, os.path.join(DIAG, '19_arquitectura_modulos.png'), Cm(1.5), Cm(3.8), Cm(21), Cm(13.6))
bullets(s, Cm(23.2), Cm(4), Cm(10), Cm(13.5), ['Entrada|Android, iOS y web abren la misma app',
                                                 'Huésped|pantallas de reserva y cuenta', 'Hotel|recepción, administración y superusuario',
                                                 'Motor|precios, validaciones, idiomas y datos', 'Externos|Firebase y geolocalización'], 13)

# =========================================================================================== 12 · concurrencia
s = slide('Rápida y sin bloquearse', '03 · Componentes síncronos y asíncronos', 'U2_E2 §9 · U35_2')
pic(s, os.path.join(DIAG, '14_concurrencia.png'), Cm(1.5), Cm(3.8), Cm(20.5), Cm(13.6))
card(s, Cm(22.6), Cm(3.9), Cm(10.3), Cm(6.3), 'Al instante (síncrono)', ['Validar datos', 'Calcular el presupuesto', 'Actualizar la pantalla'], MINT, TEAL, 13)
card(s, Cm(22.6), Cm(10.6), Cm(10.3), Cm(6.6), 'En segundo plano (asíncrono)', ['Guardar en Firebase', 'Iniciar sesión', 'Animaciones y avisos'], SAND, GOLD, 13)

# =========================================================================================== 13 · componentes externos
s = slide('Componentes externos: una oportunidad', '03 · Integración y reutilización', 'U2_E4 · U2_E5')
pic(s, os.path.join(DIAG, '09_dependencias_externas.png'), Cm(22), Cm(3.6), Cm(10.9), Cm(14))
card(s, Cm(1.5), Cm(3.9), Cm(9.9), Cm(13.3), 'Ventajas', ['Ahorro de tiempo', 'Piezas probadas por miles', 'Licencias libres', 'Aprendizaje profesional'], MINT, GREEN, 17)
card(s, Cm(11.8), Cm(3.9), Cm(9.9), Cm(13.3), 'Retos que resolvimos', ['Sin SDK de Firebase para web → REST con Ktor', 'Pruebas en Node → JVM', 'Cambios de versión → leer notas'], SAND, RED, 17)

# =========================================================================================== 14 · divisor U4
divider('04', 'Unidad 4 · Bases de datos', 'Del contexto al modelo de datos en Firebase', 'escritorio_admin_panel.jpg')

# =========================================================================================== 15 · contexto
s = slide('Diagrama de contexto', '04 · Quién intercambia datos con el sistema', 'U4_2')
pic(s, os.path.join(DIAG, '01c_contexto_simple.png'), Cm(1.5), Cm(3.7), Cm(31.4), Cm(13.9))

# =========================================================================================== 16 · DFD nivel 1
s = slide('DFD nivel 1: procesos y almacenes', '04 · Flujo de datos', 'U4_2')
pic(s, os.path.join(DIAG, '01b_dfd_nivel1.png'), Cm(1.5), Cm(3.7), Cm(18.5), Cm(13.9))
bullets(s, Cm(20.8), Cm(4), Cm(12), Cm(13.5), ['6 procesos|cuenta, cookies, reservar, recepción, catálogo, gobierno',
                                                 '7 almacenes|usuarios, habitaciones, promociones, reservas, parámetros, auditoría y dispositivo',
                                                 'Se lee por filas|cada proceso con su entidad a la izquierda y sus datos a la derecha'], 14)

# =========================================================================================== 17 · E-R Chen
s = slide('Modelo entidad-relación (Chen)', '04 · Entidades y relaciones', 'U4_3')
pic(s, os.path.join(DIAG, '02a_er_chen.png'), Cm(1.5), Cm(3.6), Cm(24.5), Cm(14))
bullets(s, Cm(26.6), Cm(4), Cm(6.4), Cm(13.5), ['Rectángulo|entidad', 'Rombo|relación', 'Óvalo|atributo', 'Línea doble|obligatoria',
                                                  '1 · N · M|cardinalidad'], 13)

# =========================================================================================== 18 · relacional y NoSQL
s = slide('Del modelo relacional a Firebase', '04 · Modelo lógico y NoSQL', 'U4_5 · U4_6')
pic(s, os.path.join(DIAG, '03_relacional.png'), Cm(1.5), Cm(3.7), Cm(15.5), Cm(13.4))
caption(s, Cm(1.5), Cm(17.1), Cm(15.5), 'Relacional normalizado (3FN)')
pic(s, os.path.join(DIAG, '11_modelo_nosql_firestore.png'), Cm(17.4), Cm(3.7), Cm(15.5), Cm(13.4))
caption(s, Cm(17.4), Cm(17.1), Cm(15.5), 'Implementación NoSQL en Firebase')

# =========================================================================================== 19 · diccionario
s = slide('Diccionario de datos: cada campo con su uso', '04 · Diccionario', 'U4_7')
table(s, Cm(1.5), Cm(3.9), Cm(31.4), [
    ['Campo', 'Qué es', 'Cuándo se usa en la plataforma'],
    ['reserva.referencia', 'Código LMB-XXXXXX', 'El huésped lo dicta en recepción al llegar'],
    ['reserva.fecha_llegada', 'Día de llegada', 'Decide en qué día aparece en "Llegadas de hoy"'],
    ['reserva.total_eur', 'Total congelado', 'Se respeta aunque el hotel suba tarifas después'],
    ['usuario.moneda', 'Moneda preferida', 'Si eligió pesos, ve MXN en cualquier dispositivo'],
    ['usuario.id_rol', 'Rol de permisos', 'Al volverse "Recepción" aparece la pestaña de llegadas'],
    ['parametro.valor', 'Regla del negocio', 'Subir el recargo de fin de semana sin actualizar la app'],
], [6.2, 6.2, 19], 14)
for i, (n_, t_) in enumerate((('60', 'campos documentados'), ('11', 'tablas relacionales'), ('6', 'colecciones en Firebase'), ('9', 'columnas por campo'))):
    x_ = Cm(1.5) + Cm(7.95) * i
    rect(s, x_, Cm(12.2), Cm(7.5), Cm(4.4), MINT if i % 2 == 0 else SAND, MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x_ + Cm(0.6), Cm(12.6), Cm(6.5), Cm(2), n_, 34, TEAL, True, SERIF)
    text(s, x_ + Cm(0.6), Cm(14.6), Cm(6.5), Cm(1.5), t_, 14, NAVY, True)

# =========================================================================================== 20 · criterios y costos
s = slide('Por qué Firebase y cuánto cuesta', '04 · Criterios de selección y costos', 'U4_4 · U4_5')
table(s, Cm(1.5), Cm(3.9), Cm(15.5), [['Candidato', 'Puntaje /5'], ['Firebase', '4.80'], ['PostgreSQL (Supabase)', '4.40'],
                                      ['MongoDB Atlas', '3.85'], ['MySQL autoalojado', '3.05'], ['SQLite', '2.95'], ['SQL Server Express', '2.90']], [11, 4.5], 13)
table(s, Cm(17.6), Cm(3.9), Cm(15.3), [['Escenario', 'Año 1'], ['Actual (Spark + Pages + APK)', '0 USD'],
                                       ['+ dominio y Google Play', '≈ 40 USD'], ['+ App Store', '≈ 140 USD'], ['PostgreSQL en VPS', '≈ 70–165 USD']], [10.3, 5], 13)
text(s, Cm(17.6), Cm(8.9), Cm(15.3), Cm(1.2), 'Precios de referencia aproximados; verificar en cada proveedor.', 11, GREY)
card(s, Cm(1.5), Cm(11.0), Cm(15.5), Cm(6.4), 'Ventajas de Firebase', ['0 € y sin servidor propio', 'Cuentas y reglas de seguridad listas', 'Mismo acceso en Android, iOS y web'], MINT, GREEN, 14)
card(s, Cm(17.6), Cm(11.0), Cm(15.3), Cm(6.4), 'Desventajas', ['Sin JOIN: algunos datos se duplican', 'Depende de Google', 'Respaldos manuales en el plan gratuito'], SAND, RED, 14)

# =========================================================================================== 21 · seguridad
s = slide('Seguridad y manejo de datos', '04 · Acceso a datos seguro', 'U2_E1 §17')
pic(s, os.path.join(DIAG, '13_reglas_firebase.png'), Cm(1.5), Cm(3.7), Cm(10.5), Cm(13.9))
card(s, Cm(12.5), Cm(3.9), Cm(10), Cm(13.3), 'Qué protegemos', ['Contraseñas: nunca en la base de datos', 'Cada quien ve solo lo suyo',
                                                                   'Nadie se asigna un rol', 'Ubicación: no se guarda', 'Historial de cambios inmutable'], MINT, TEAL, 13)
pic(s, os.path.join(SHOT, 'escritorio_super_seguridad.jpg'), Cm(23), Cm(3.9), Cm(9.9), Cm(6.4))
pic(s, os.path.join(SHOT, 'movil_cookies.jpg'), Cm(25.2), Cm(10.6), Cm(5.5), Cm(7))

# =========================================================================================== 22 · móvil vs web
s = slide('Qué tiene el móvil que la web no, y al revés', '05 · Móvil y web', 'U2_E1 §18')
cols = [('Solo móvil', GOLD, SAND, ['Llave digital de la habitación', 'Uso de pie y de viaje', 'Pensado para el pulgar'],
         'movil_mis_reservas.jpg', 'En web se avisa: "Llave digital en la app móvil"'),
        ('En ambos', TEAL, MINT, ['Reservar en 3 pasos', 'Mis reservas y cancelar', 'Ofertas, cuenta y cookies', 'Recepción (personal)'],
         'movil_reserva_extras.jpg', 'Misma reserva en teléfono y web'),
        ('Solo web', NAVY, PAPER, ['Panel de administración', 'Catálogo y promociones', 'Superusuario: roles y parámetros', 'Tablas e indicadores'],
         'escritorio_admin_panel.jpg', 'Panel de administración')]
for i, (t, col, fill, items, img, cap) in enumerate(cols):
    x = Cm(1.5) + Cm(10.6) * i
    rect(s, x, Cm(3.8), Cm(10.2), Cm(13.8), fill, MSO_SHAPE.ROUNDED_RECTANGLE, LINE)
    text(s, x + Cm(0.5), Cm(4.1), Cm(9), Cm(1), t, 17, col, True)
    bullets(s, x + Cm(0.5), Cm(5.2), Cm(9.3), Cm(4.5), items, 12, NAVY, 3)
    if 'escritorio' in img:
        pic(s, os.path.join(SHOT, img), x + Cm(0.3), Cm(9.7), Cm(9.6), Cm(6.6))
    else:
        pic(s, os.path.join(SHOT, img), x + Cm(2.6), Cm(9.5), Cm(5), Cm(7))
    caption(s, x, Cm(16.6), Cm(10.2), cap)

# =========================================================================================== 23 · roles y paneles
s = slide('Paneles según el rol', '05 · Web completa para el personal', 'U2_E3 §6')
for j, (f, c_) in enumerate((('escritorio_recepcion.jpg', 'Recepción: llegadas y salidas del día'),
                             ('escritorio_admin_catalogo.jpg', 'Administrador: precios y disponibilidad'),
                             ('escritorio_super_parametros.jpg', 'Superusuario: parámetros sin publicar versión'))):
    x = Cm(1.5) + Cm(10.6) * j
    pic(s, os.path.join(SHOT, f), x, Cm(4), Cm(10.2), Cm(7.2))
    caption(s, x, Cm(11.3), Cm(10.2), c_)
for i, t in enumerate(('Huésped', 'Recepción', 'Administrador', 'Superusuario')):
    chip(s, Cm(1.5) + Cm(7.95) * i, Cm(13.2), Cm(7.5), t, MINT)
text(s, Cm(1.5), Cm(14.6), Cm(31.4), Cm(2.5), 'Cada nivel incluye lo del anterior. Solo el superusuario puede cambiar roles, y las reglas de Firebase lo hacen cumplir en el servidor.', 14, NAVY, False, SANS, PP_ALIGN.CENTER)

# =========================================================================================== 24 · resultados
s = slide('Resultados', '06 · Resultados', 'Documentos U35_1 a U35_4')
table(s, Cm(1.5), Cm(3.9), Cm(20), [['Tema', 'Qué logramos'],
                                    ['Interfaz gráfica', '14 pantallas, retroalimentación inmediata, adaptable'],
                                    ['Síncrono / asíncrono', 'Corrutinas, Flows y Ktor; la UI nunca se bloquea'],
                                    ['Acceso a datos', 'Firebase con reglas por rol y copia local'],
                                    ['Propuesta móvil', 'Oportunidad, persona, funciones y KMP']], [6.5, 13.5], 13)
for i, (n, t) in enumerate((('14', 'pruebas en verde'), ('20', 'documentos + video'), ('< 1 min', 'para reservar'), ('0 €', 'de operación'))):
    y = Cm(3.9) + Cm(3.4) * i
    rect(s, Cm(22.4), y, Cm(10.5), Cm(3), MINT if i % 2 == 0 else SAND, MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, Cm(23), y + Cm(0.35), Cm(5), Cm(2), n, 30, TEAL, True, SERIF)
    text(s, Cm(27.6), y + Cm(0.95), Cm(5.2), Cm(1.4), t, 14, NAVY, True)

# =========================================================================================== 25 · cierre
num[0] += 1
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
text(s, Cm(2), Cm(2.6), Cm(20), Cm(2.5), '¡Gracias!', 56, WHITE, True, SERIF)
bullets(s, Cm(2), Cm(6.2), Cm(20), Cm(7), ['Aprendimos|una interfaz es buena cuando el usuario se recupera solo de sus errores.',
                                             'Seguridad|vive en el servidor; la app solo mejora la experiencia.',
                                             'Siguiente paso|pagos de prueba, notificaciones y pruebas de UI.'], 16, WHITE, 9, RGBColor(0x8F, 0xDD, 0xE2))
text(s, Cm(2), Cm(13.4), Cm(21), Cm(4), ['App web · jancarliux24.github.io/hotel-lumbre/app', 'Diagramas · ' + VISOR,
                                          'Código · github.com/JanCarliux24/hotel-lumbre'], 14, SUN, True)
pic(s, os.path.join(SHOT, 'qr_descargas.png'), Cm(22.6), Cm(5.2), Cm(10.4), Cm(6.65))
text(s, Cm(22.6), Cm(12.3), Cm(10.4), Cm(1), 'Escanea para descargar la APK o abrir la web', 12, WHITE, True, SANS, PP_ALIGN.CENTER)
footer(s, True)

assert num[0] == TOTAL, num[0]
prs.save(OUT)
print(OUT, len(prs.slides), 'diapositivas')
