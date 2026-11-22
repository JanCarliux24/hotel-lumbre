"""Diagrama entidad-relación en notación de Chen, dibujado con posiciones fijas (sin cruces).

Rectángulos = entidades · rombos = relaciones · óvalos = atributos (subrayado = clave, punteado = derivado,
doble = multivaluado). Línea doble = participación total. Genera SVG (vectorial, zoom sin pérdida) y PNG.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'diagramas')
FONT = os.path.join(ROOT, 'app', 'shared', 'src', 'commonMain', 'composeResources', 'font', 'inter.ttf')

W, H = 3300, 2700
C_ENT, S_ENT = '#DDF3F4', '#0A7C86'
C_REL, S_REL = '#FBEDE6', '#B87A63'
C_ATT, S_ATT = '#FCE7BF', '#D9A441'
C_KEY = '#F9D98C'
LINE, TEXT = '#5B6E73', '#16313A'

# ------------------------------------------------------------------ modelo
ENT = {  # nombre: (x, y, atributos)  · atributo: (texto, tipo) tipo k=clave, d=derivado, n=normal
    'ROL': (400, 450, [('id_rol', 'k'), ('nombre', 'n'), ('nivel', 'n')]),
    'USUARIO': (1550, 450, [('id_usuario', 'k'), ('correo', 'n'), ('nombre', 'n'), ('telefono', 'n'), ('idioma', 'n'),
                            ('moneda', 'n'), ('tema', 'n'), ('bloqueado', 'n'), ('fecha_alta', 'n'), ('ultimo_acceso', 'n')]),
    'AUDITORIA': (2850, 450, [('id_auditoria', 'k'), ('fecha_hora', 'n'), ('accion', 'n'), ('objetivo', 'n')]),
    'PARAMETRO': (2850, 950, [('clave', 'k'), ('valor', 'n'), ('descripcion', 'n')]),
    'RESERVA': (1550, 1500, [('referencia', 'k'), ('contacto', 'c'),
                             ('fecha_llegada', 'n'), ('fecha_salida', 'n'), ('noches', 'd'), ('adultos', 'n'), ('ninos', 'n'),
                             ('total_eur', 'n'), ('estado', 'n'), ('notas', 'n'), ('fecha_creacion', 'n')]),
    'TIPO_HABITACION': (450, 1500, [('id_tipo', 'k'), ('nombre', 'n'), ('descripcion', 'n'), ('superficie_m2', 'n'),
                                     ('capacidad', 'n'), ('precio_noche_eur', 'n'), ('disponible', 'n')]),
    'AMENIDAD': (450, 2380, [('id_amenidad', 'k'), ('nombre', 'n')]),
    'PROMOCION': (1550, 2400, [('codigo', 'k'), ('porcentaje', 'n'), ('activa', 'n')]),
    'EXTRA': (2850, 1500, [('id_extra', 'k'), ('nombre', 'n'), ('precio_eur', 'n'), ('unidad_cobro', 'n')]),
}
# relación: (x, y, entidad A, card A, total A, entidad B, card B, total B, atributos)
REL = {
    'ASIGNA': (950, 450, 'ROL', '1', False, 'USUARIO', 'N', True, []),
    'GENERA': (2200, 450, 'USUARIO', '1', False, 'AUDITORIA', 'N', True, []),
    'MODIFICA': (2200, 950, 'USUARIO', '1', False, 'PARAMETRO', 'N', False, [('fecha_modificacion', 'n')]),
    'REALIZA': (1550, 950, 'USUARIO', '1', False, 'RESERVA', 'N', False, []),
    'SE_RESERVA_EN': (1000, 1500, 'TIPO_HABITACION', '1', False, 'RESERVA', 'N', True, []),
    'OFRECE': (450, 1980, 'TIPO_HABITACION', 'N', False, 'AMENIDAD', 'M', False, []),
    'SE_APLICA_A': (1550, 2000, 'PROMOCION', '1', False, 'RESERVA', 'N', False, []),
    'INCLUYE': (2200, 1500, 'RESERVA', 'N', False, 'EXTRA', 'M', False, [('importe_eur', 'n')]),
}
COMPUESTOS = {'contacto': [('nombre_huesped', 'n'), ('correo_contacto', 'n'), ('telefono_contacto', 'n')]}
EW, EH = 250, 74          # entidad
RW, RH = 230, 120         # rombo


def text_w(t, size=24):
    return ImageFont.truetype(FONT, size).getlength(t)


def oval_size(t):
    return text_w(t) + 44, 56


# ------------------------------------------------------------------ geometría y colocación automática de atributos
shapes = []  # cajas ocupadas (x0, y0, x1, y1)
for n, (x, y, _) in ENT.items():
    shapes.append((x - EW / 2, y - EH / 2, x + EW / 2, y + EH / 2))
for n, (x, y, *_r) in REL.items():
    shapes.append((x - RW / 2, y - RH / 2, x + RW / 2, y + RH / 2))
segments = []
shapes.append((W - 850, H - 520, W, H))  # leyenda
for n, (x, y, a, ca, ta, b, cb, tb, _) in REL.items():
    segments.append((x, y, *ENT[a][:2]))
    segments.append((x, y, *ENT[b][:2]))


def overlap(b1, b2, m=10):
    return not (b1[2] + m < b2[0] or b2[2] + m < b1[0] or b1[3] + m < b2[1] or b2[3] + m < b1[1])


def seg_hits_box(s, b):
    x0, y0, x1, y1 = s
    for i in range(1, 30):
        t = i / 30
        px, py = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if b[0] - 6 < px < b[2] + 6 and b[1] - 6 < py < b[3] + 6:
            return True
    return False


def rel_angles(name):
    """Direcciones (grados) de las líneas que salen de una entidad o relación hacia sus vecinos."""
    out = []
    for n, (x, y, a, ca, ta, b, cb, tb, _) in REL.items():
        if name == n:
            for e in (a, b):
                ex, ey = ENT[e][:2]; out.append(math.degrees(math.atan2(ey - y, ex - x)))
        elif name in (a, b):
            ex, ey = ENT[name][:2]; out.append(math.degrees(math.atan2(y - ey, x - ex)))
    return out


def cross(s1, s2):
    """True si los segmentos se cruzan (sin contar los que comparten extremo)."""
    (x1, y1, x2, y2), (x3, y3, x4, y4) = s1, s2
    if (abs(x1 - x3) < 1 and abs(y1 - y3) < 1) or (abs(x1 - x4) < 1 and abs(y1 - y4) < 1):
        return False
    def o(ax, ay, bx, by, cx, cy):
        return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    d1, d2 = o(x3, y3, x4, y4, x1, y1), o(x3, y3, x4, y4, x2, y2)
    d3, d4 = o(x1, y1, x2, y2, x3, y3), o(x1, y1, x2, y2, x4, y4)
    return d1 * d2 < 0 and d3 * d4 < 0


def place(cx, cy, attrs, own_box, name, blocked=None):
    placed = []
    n = len(attrs)
    blocked = rel_angles(name) if blocked is None else blocked
    free = [a for a in range(0, 360) if all(min(abs(a - b) % 360, 360 - abs(a - b) % 360) > 13 for b in blocked)]
    for i, (t, kind) in enumerate(attrs):
        w, h = oval_size(t)
        base = free[int((i + 0.5) * len(free) / n) % len(free)]
        cands = sorted(free, key=lambda a: min(abs(a - base), 360 - abs(a - base)))
        best = None
        for r in (range(210, 900, 12) if name else range(120, 600, 10)):
            for a_ in cands:
                ang = math.radians(a_)
                ox, oy = cx + r * math.cos(ang) * 1.2, cy + r * math.sin(ang) * 0.95
                box = (ox - w / 2, oy - h / 2, ox + w / 2, oy + h / 2)
                if box[0] < 10 or box[2] > W - 10 or box[1] < 80 or box[3] > H - 10:
                    continue
                if any(overlap(box, s) for s in shapes):
                    continue
                link = (cx, cy, ox, oy)
                if any(seg_hits_box(link, s) for s in shapes if s != own_box):
                    continue
                if any(seg_hits_box(sg, box) for sg in segments):
                    continue
                if any(cross(link, sg) for sg in segments):
                    continue
                best = (ox, oy, box, link); break
            if best:
                break
        if best is None:
            raise SystemExit(f'No cabe el atributo {t} de {name}')
        ox, oy, box, link = best
        shapes.append(box); segments.append(link)
        placed.append((t, kind, ox, oy, w, h))
        if kind == 'c':  # atributo compuesto: sus partes alrededor, sin volver hacia la entidad
            back = math.degrees(math.atan2(cy - oy, cx - ox))
            for sub in place(ox, oy, COMPUESTOS[t], box, None, [back]):
                placed.append(sub + ((ox, oy),))
    return placed


ATTR = {}
for n, (x, y, attrs) in sorted(ENT.items(), key=lambda kv: -len(kv[1][2])):
    ATTR[n] = place(x, y, attrs, (x - EW / 2, y - EH / 2, x + EW / 2, y + EH / 2), n)
for n, (x, y, *_r, attrs) in REL.items():
    ATTR[n] = place(x, y, attrs, (x - RW / 2, y - RH / 2, x + RW / 2, y + RH / 2), n)


# ------------------------------------------------------------------ SVG
def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;')


def svg():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Inter, Segoe UI, sans-serif">',
         '<rect width="100%" height="100%" fill="#FFFFFF"/>',
         f'<text x="{W/2}" y="48" text-anchor="middle" font-size="34" font-weight="700" fill="{TEXT}">Modelo entidad-relación (notación de Chen) — Lumbre Hotel &amp; Spa</text>']
    # líneas atributo
    for n, items in ATTR.items():
        cx, cy = (ENT[n][:2] if n in ENT else REL[n][:2])
        for it in items:
            t, kind, ox, oy, w, h = it[:6]
            px, py = it[6] if len(it) > 6 else (cx, cy)
            o.append(f'<line x1="{px}" y1="{py}" x2="{ox}" y2="{oy}" stroke="{LINE}" stroke-width="2"/>')
    # líneas relación con cardinalidad
    for n, (x, y, a, ca, ta, b, cb, tb, _) in REL.items():
        for ent, card, total in ((a, ca, ta), (b, cb, tb)):
            ex, ey = ENT[ent][:2]
            if total:
                dx, dy = ex - x, ey - y; L = math.hypot(dx, dy); nx, ny = -dy / L * 5, dx / L * 5
                for s in (1, -1):
                    o.append(f'<line x1="{x+nx*s}" y1="{y+ny*s}" x2="{ex+nx*s}" y2="{ey+ny*s}" stroke="{TEXT}" stroke-width="2.4"/>')
            else:
                o.append(f'<line x1="{x}" y1="{y}" x2="{ex}" y2="{ey}" stroke="{TEXT}" stroke-width="2.6"/>')
            mx, my = x + (ex - x) * 0.5, y + (ey - y) * 0.5
            o.append(f'<circle cx="{mx}" cy="{my}" r="19" fill="#FFFFFF" stroke="{S_ENT}" stroke-width="2"/>')
            o.append(f'<text x="{mx}" y="{my+8}" text-anchor="middle" font-size="22" font-weight="700" fill="{S_ENT}">{card}</text>')
    # óvalos
    for n, items in ATTR.items():
        for it in items:
            t, kind, ox, oy, w, h = it[:6]
            dash = ' stroke-dasharray="8 6"' if kind == 'd' else ''
            fill = C_KEY if kind == 'k' else C_ATT
            o.append(f'<ellipse cx="{ox}" cy="{oy}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{S_ATT}" stroke-width="2"{dash}/>')
            deco = ' text-decoration="underline" font-weight="700"' if kind == 'k' else ''
            o.append(f'<text x="{ox}" y="{oy+8}" text-anchor="middle" font-size="24" fill="{TEXT}"{deco}>{esc(t)}</text>')
    # rombos
    for n, (x, y, *_r) in REL.items():
        pts = f'{x},{y-RH/2} {x+RW/2},{y} {x},{y+RH/2} {x-RW/2},{y}'
        o.append(f'<polygon points="{pts}" fill="{C_REL}" stroke="{S_REL}" stroke-width="2.6"/>')
        label = n.replace('_', ' ')
        o.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="21" font-weight="700" fill="{TEXT}">{esc(label)}</text>')
    # entidades
    for n, (x, y, _) in ENT.items():
        o.append(f'<rect x="{x-EW/2}" y="{y-EH/2}" width="{EW}" height="{EH}" rx="6" fill="{C_ENT}" stroke="{S_ENT}" stroke-width="3"/>')
        o.append(f'<text x="{x}" y="{y+9}" text-anchor="middle" font-size="26" font-weight="700" fill="{TEXT}">{esc(n)}</text>')
    # leyenda
    lx, ly = W - 830, H - 510
    o.append(f'<rect x="{lx}" y="{ly}" width="800" height="490" rx="18" fill="#FAFCFC" stroke="#CFE3E5" stroke-width="2"/>')
    o.append(f'<text x="{lx+30}" y="{ly+50}" font-size="26" font-weight="700" fill="{TEXT}">Simbología</text>')
    items = [('rect', 'Entidad'), ('diamond', 'Relación'), ('key', 'Atributo clave (subrayado)'), ('oval', 'Atributo'),
             ('dash', 'Atributo derivado (noches = salida − llegada)'), ('comp', 'Atributo compuesto (contacto → nombre, correo, teléfono)'), ('double', 'Participación total (obligatoria)'), ('card', 'Cardinalidad 1 · N · M')]
    for i, (k, t) in enumerate(items):
        y0 = ly + 95 + i * 50; x0 = lx + 40
        if k == 'rect': o.append(f'<rect x="{x0}" y="{y0-18}" width="70" height="34" rx="4" fill="{C_ENT}" stroke="{S_ENT}" stroke-width="2"/>')
        if k == 'diamond': o.append(f'<polygon points="{x0+35},{y0-22} {x0+70},{y0} {x0+35},{y0+22} {x0},{y0}" fill="{C_REL}" stroke="{S_REL}" stroke-width="2"/>')
        if k == 'comp':
            o.append(f'<ellipse cx="{x0+35}" cy="{y0}" rx="35" ry="18" fill="{C_ATT}" stroke="{S_ATT}" stroke-width="2"/><line x1="{x0+70}" y1="{y0}" x2="{x0+88}" y2="{y0-14}" stroke="{LINE}" stroke-width="2"/>')
        if k in ('key', 'oval', 'dash'):
            d = ' stroke-dasharray="6 5"' if k == 'dash' else ''
            o.append(f'<ellipse cx="{x0+35}" cy="{y0}" rx="35" ry="18" fill="{C_KEY if k=="key" else C_ATT}" stroke="{S_ATT}" stroke-width="2"{d}/>')
        if k == 'double':
            o.append(f'<line x1="{x0}" y1="{y0-4}" x2="{x0+70}" y2="{y0-4}" stroke="{TEXT}" stroke-width="2"/><line x1="{x0}" y1="{y0+4}" x2="{x0+70}" y2="{y0+4}" stroke="{TEXT}" stroke-width="2"/>')
        if k == 'card':
            o.append(f'<circle cx="{x0+35}" cy="{y0}" r="17" fill="#FFF" stroke="{S_ENT}" stroke-width="2"/><text x="{x0+35}" y="{y0+7}" text-anchor="middle" font-size="19" font-weight="700" fill="{S_ENT}">N</text>')
        o.append(f'<text x="{x0+95}" y="{y0+8}" font-size="22" fill="{TEXT}">{esc(t)}</text>')
    o.append('</svg>')
    return '\n'.join(o)


# ------------------------------------------------------------------ PNG (mismo dibujo con Pillow, 2x)
def png(path, s=2):
    im = Image.new('RGB', (W * s, H * s), 'white'); d = ImageDraw.Draw(im)
    F = lambda size, bold=False: ImageFont.truetype(FONT, int(size * s))
    def f(size, bold):
        ft = F(size)
        try: ft.set_variation_by_name('Bold' if bold else 'Regular')
        except Exception: pass
        return ft
    def ctext(x, y, t, size, bold=False, color=TEXT, underline=False):
        ft = f(size, bold); tw = ft.getlength(t)
        d.text((x * s - tw / 2, y * s), t, font=ft, fill=color, anchor='lm')
        if underline: d.line([(x * s - tw / 2, (y + 15) * s), (x * s + tw / 2, (y + 15) * s)], fill=color, width=2 * s)
    ctext(W / 2, 40, 'Modelo entidad-relación (notación de Chen) — Lumbre Hotel & Spa', 34, True)
    for n, items in ATTR.items():
        cx, cy = (ENT[n][:2] if n in ENT else REL[n][:2])
        for t, kind, ox, oy, w, h in items:
            d.line([(cx * s, cy * s), (ox * s, oy * s)], fill=LINE, width=2 * s)
    for n, (x, y, a, ca, ta, b, cb, tb, _) in REL.items():
        for ent, card, total in ((a, ca, ta), (b, cb, tb)):
            ex, ey = ENT[ent][:2]
            if total:
                dx, dy = ex - x, ey - y; L = math.hypot(dx, dy); nx, ny = -dy / L * 5, dx / L * 5
                for k in (1, -1):
                    d.line([((x + nx * k) * s, (y + ny * k) * s), ((ex + nx * k) * s, (ey + ny * k) * s)], fill=TEXT, width=int(2.4 * s))
            else:
                d.line([(x * s, y * s), (ex * s, ey * s)], fill=TEXT, width=int(2.6 * s))
            mx, my = (x + ex) / 2, (y + ey) / 2
            d.ellipse([(mx - 19) * s, (my - 19) * s, (mx + 19) * s, (my + 19) * s], fill='white', outline=S_ENT, width=2 * s)
            ctext(mx, my, card, 22, True, S_ENT)
    for n, items in ATTR.items():
        for t, kind, ox, oy, w, h in items:
            box = [(ox - w / 2) * s, (oy - h / 2) * s, (ox + w / 2) * s, (oy + h / 2) * s]
            d.ellipse(box, fill=C_KEY if kind == 'k' else C_ATT, outline=S_ATT, width=2 * s)
            if kind == 'd':  # punteado: se marca con huecos blancos sobre el borde
                for a in range(0, 360, 14):
                    r1 = math.radians(a)
                    px, py = ox + (w / 2) * math.cos(r1), oy + (h / 2) * math.sin(r1)
                    d.ellipse([(px - 3) * s, (py - 3) * s, (px + 3) * s, (py + 3) * s], fill='white')
            ctext(ox, oy, t, 24, kind == 'k', TEXT, kind == 'k')
    for n, (x, y, *_r) in REL.items():
        pts = [(x * s, (y - RH / 2) * s), ((x + RW / 2) * s, y * s), (x * s, (y + RH / 2) * s), ((x - RW / 2) * s, y * s)]
        d.polygon(pts, fill=C_REL, outline=S_REL, width=3 * s)
        ctext(x, y, n.replace('_', ' '), 21, True)
    for n, (x, y, _) in ENT.items():
        d.rounded_rectangle([(x - EW / 2) * s, (y - EH / 2) * s, (x + EW / 2) * s, (y + EH / 2) * s], 6 * s, fill=C_ENT, outline=S_ENT, width=3 * s)
        ctext(x, y, n, 26, True)
    im.save(path, optimize=True)


open(os.path.join(OUT, '02a_er_chen.svg'), 'w', encoding='utf-8').write(svg())
# PNG: se rasteriza el SVG con raster_svg.py (idéntico al vectorial)
print('ok')
