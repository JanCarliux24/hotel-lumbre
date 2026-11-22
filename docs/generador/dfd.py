"""Diagramas de flujo de datos (Yourdon/DeMarco) con posiciones fijas y líneas ortogonales: nivel 0 y nivel 1.
Genera SVG (vectorial); el PNG se obtiene con raster_svg.py."""
import math, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'diagramas')
TEAL, NAVY, SUN, GREY = '#0A7C86', '#16313A', '#D9A441', '#5B6E73'
STY = {'ext': ('#FFF4E2', '#B87A1E'), 'svc': ('#E6F6FA', '#0A7C86'), 'proc': ('#D6F3F2', '#0A7C86'), 'store': ('#FFFCF5', '#B87A1E')}


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;')


class Dia:
    def __init__(self, w, h, title, subtitle='', dy=0):
        self.w, self.h, self.dy = w, h + dy, dy
        self.back, self.front, self.labels = [], [], []
        self.title, self.subtitle = title, subtitle

    def text(self, x, y, lines, size=22, weight=400, color=NAVY, anchor='middle', layer=None):
        lines = lines if isinstance(lines, list) else [lines]
        y0 = y - (len(lines) - 1) * size * 0.6
        for i, ln in enumerate(lines):
            (layer if layer is not None else self.front).append(
                f'<text x="{x}" y="{y0 + i * size * 1.2 + size * 0.35}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{color}">{esc(ln)}</text>')

    def node(self, kind, x, y, w, h, title, lines):
        f, s = STY[kind]
        if kind == 'proc':
            r = w / 2
            self.front.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{s}" stroke-width="3"/>')
            self.front.append(f'<line x1="{x - r * 0.82}" y1="{y - r * 0.42}" x2="{x + r * 0.82}" y2="{y - r * 0.42}" stroke="{s}" stroke-width="2"/>')
            self.text(x, y - r * 0.62, title, 22, 700, TEAL)
            self.text(x, y + r * 0.12, lines, 21, 600)
        elif kind == 'store':
            x0, y0 = x - w / 2, y - h / 2
            self.front.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{f}" stroke="none"/>')
            self.front.append(f'<path d="M{x0 + w} {y0} H{x0} V{y0 + h} H{x0 + w}" fill="none" stroke="{s}" stroke-width="3"/>')
            self.front.append(f'<line x1="{x0 + 80}" y1="{y0}" x2="{x0 + 80}" y2="{y0 + h}" stroke="{s}" stroke-width="2"/>')
            self.text(x0 + 40, y, title, 22, 700, '#8A5A12')
            self.text(x0 + 80 + (w - 80) / 2, y, lines, 21, 600)
        else:
            x0, y0 = x - w / 2, y - h / 2
            self.front.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="{f}" stroke="{s}" stroke-width="3"/>')
            self.text(x, y - h / 2 + 30, title, 20, 700, s)
            self.text(x, y + 14, lines, 22, 600)

    def edge(self, pts, label=None, at=None, side=-1, color=TEAL, dashed=False):
        d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
        da = ' stroke-dasharray="10 7"' if dashed else ''
        self.back.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.6" stroke-linejoin="round"{da}/>')
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        a = math.atan2(y2 - y1, x2 - x1); L = 18
        p1 = (x2 - L * math.cos(a - 0.38), y2 - L * math.sin(a - 0.38)); p2 = (x2 - L * math.cos(a + 0.38), y2 - L * math.sin(a + 0.38))
        self.back.append(f'<polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{color}"/>')
        if label:
            if at is None:  # punto medio del tramo más largo
                segs = list(zip(pts, pts[1:]))
                (ax, ay), (bx, by) = max(segs, key=lambda s: math.hypot(s[1][0] - s[0][0], s[1][1] - s[0][1]))
                at = ((ax + bx) / 2, (ay + by) / 2 + side * 20)
            lines = label if isinstance(label, list) else [label]
            wmax = max(len(l) for l in lines) * 10.2 + 16
            hh = len(lines) * 23 + 8
            self.labels.append(f'<rect x="{at[0] - wmax / 2}" y="{at[1] - hh / 2}" width="{wmax}" height="{hh}" rx="6" fill="#FFFFFF" fill-opacity="0.92"/>')
            self.text(at[0], at[1], lines, 18, 500, NAVY, layer=self.labels)

    def save(self, name, notes=None):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="Inter, Segoe UI, sans-serif">',
             '<rect width="100%" height="100%" fill="#FFFFFF"/>']
        o.append(f'<text x="{self.w / 2}" y="52" text-anchor="middle" font-size="34" font-weight="700" fill="{NAVY}">{esc(self.title)}</text>')
        if self.subtitle:
            o.append(f'<text x="{self.w / 2}" y="88" text-anchor="middle" font-size="20" fill="{GREY}">{esc(self.subtitle)}</text>')
        o.append(f'<g transform="translate(0,{self.dy})">')
        o += self.back + self.front + self.labels
        o.append('</g>')
        o.append('</svg>')
        open(os.path.join(OUT, name + '.svg'), 'w', encoding='utf-8').write('\n'.join(o))


def pair(d, a, b, off, lab_ab, lab_ba, horiz=True, la=None, lb=None):
    """Dos flujos paralelos en sentidos opuestos entre los puntos a y b."""
    (ax, ay), (bx, by) = a, b
    if horiz:
        d.edge([(ax, ay - off), (bx, by - off)], lab_ab, la, -1)
        d.edge([(bx, by + off), (ax, ay + off)], lab_ba, lb, 1)
    else:
        d.edge([(ax - off, ay), (bx - off, by)], lab_ab, la)
        d.edge([(bx + off, by), (ax + off, ay)], lab_ba, lb)


# ====================================================================================== NIVEL 0
def nivel0():
    d = Dia(2620, 1960, 'Diagrama de contexto (DFD nivel 0) — Lumbre Hotel & Spa',
            'Notación Yourdon/DeMarco · el sistema completo es el proceso 0 · flujos F1–F14')
    cx, cy, R = 1300, 960, 200
    d.node('proc', cx, cy, 2 * R, 2 * R, '0', ['Sistema de reservas', 'Lumbre Hotel & Spa', 'Android · iOS · web', '+ base de datos Firebase'])
    ents = {
        'E1': ('ext', 260, 960, 300, 130, 'E1', ['Huésped / visitante']),
        'E2': ('ext', 420, 330, 300, 130, 'E2', ['Recepción (STAFF)']),
        'E3': ('ext', 1300, 230, 320, 130, 'E3', ['Administrador (ADMIN)']),
        'E4': ('ext', 2180, 330, 340, 130, 'E4', ['Superusuario', '(SUPERADMIN)']),
        'E5': ('svc', 2300, 960, 320, 130, 'E5', ['Firebase Authentication']),
        'E6': ('svc', 2180, 1600, 320, 130, 'E6', ['Geolocalización', '(BigDataCloud)']),
        'E8': ('svc', 1300, 1720, 340, 130, 'E8', ['SO / navegador', '(permiso de ubicación)']),
        'E7': ('svc', 420, 1600, 320, 130, 'E7', ['Correo de Firebase']),
    }
    for k, (kind, x, y, w, h, t, ls) in ents.items():
        d.node(kind, x, y, w, h, t, ls)

    def border(x, y, tx, ty, r):  # punto en el borde del círculo hacia (tx, ty)
        a = math.atan2(ty - y, tx - x); return x + r * math.cos(a), y + r * math.sin(a)

    def link(ent, lab_in, lab_out, off=20):
        kind, x, y, w, h, *_ = ents[ent]
        a = math.atan2(cy - y, cx - x)
        nx, ny = -math.sin(a) * off, math.cos(a) * off
        dx, dy = cx - x, cy - y
        t = min((w / 2 + 6) / abs(dx) if abs(dx) > 1e-6 else 1e9, (h / 2 + 6) / abs(dy) if abs(dy) > 1e-6 else 1e9)
        ex, ey = x + dx * t, y + dy * t
        px, py = border(cx, cy, x, y, R + 6)
        k = 8.5 if abs(math.cos(a)) < 0.35 else 3.2
        nx2, ny2 = nx * k / 3.2, ny * k / 3.2
        nx, ny = nx, ny
        if lab_in:
            d.edge([(ex + nx, ey + ny), (px + nx, py + ny)], lab_in, ((ex + px) / 2 + nx2 * 3.2, (ey + py) / 2 + ny2 * 3.2))
        if lab_out:
            d.edge([(px - nx, py - ny), (ex - nx, ey - ny)], lab_out, ((ex + px) / 2 - nx2 * 3.2, (ey + py) / 2 - ny2 * 3.2))

    link('E1', ['F1 datos de reserva', 'F2 consentimiento, credenciales'], ['F3 presupuesto, referencia,', 'mis reservas, avisos'], 22)
    link('E2', ['F4 registro de llegada,', 'cancelación'], ['F5 llegadas / en el hotel /', 'salidas del día'])
    link('E3', ['F6 precios, disponibilidad,', 'promociones'], ['F7 indicadores, ingresos'])
    link('E4', ['F8 roles, bloqueo,', 'parámetros'], ['F9 usuarios, auditoría,', 'seguridad'])
    link('E5', ["F10' UID + tokens"], ['F10 alta, inicio de sesión,', 'renovación de token'])
    link('E6', ["F11' código de país"], ['F11 lat/lon redondeadas', '(~11 km)'])
    link('E8', ["F14' coordenadas o rechazo"], ['F14 solicitud de permiso'])
    # E5 → E7 → E1 (correo)
    d.edge([(2466, 960), (2560, 960), (2560, 1840), (420, 1840), (420, 1671)], 'F12 solicitud de correo (Firebase envía el mensaje)', (1500, 1840))
    d.edge([(330, 1535), (330, 1025)], ['F13 correo', 'con enlace'], (230, 1280))
    d.text(1300, 1920, 'Límite del sistema: interfaz de las 3 plataformas + reglas de negocio + sincronización + Cloud Firestore con sus reglas.', 19, 400, GREY)
    d.save('01_contexto')


# ====================================================================================== NIVEL 1
def nivel1():
    d = Dia(2560, 2250, 'DFD nivel 1 — explosión del proceso 0',
            'Entidades a la izquierda · procesos al centro · almacenes a la derecha · los flujos entre filas usan carriles verticales', 60)
    XE, XP, XS, XR = 230, 720, 1560, 2250
    PR = 100  # radio de proceso
    procs = {'P1': 260, 'P2': 600, 'P3': 980, 'P4': 1360, 'P5': 1700, 'P6': 2040}
    ptxt = {'P1': ('1.0', ['Gestionar cuenta', 'y sesión']), 'P2': ('2.0', ['Consentimiento,', 'idioma y moneda']),
            'P3': ('3.0', ['Cotizar y', 'reservar']), 'P4': ('4.0', ['Operar', 'recepción']),
            'P5': ('5.0', ['Administrar', 'catálogo']), 'P6': ('6.0', ['Gobernar sistema', 'y auditar'])}
    for k, y in procs.items():
        d.node('proc', XP, y, 2 * PR, 2 * PR, *ptxt[k])
    SW, SH = 420, 76
    stores = {'D1': (260, 'users'), 'D7': (470, 'almacenamiento local'), 'D2': (860, 'rooms'), 'D3': (980, 'promos'),
              'D5': (1100, 'config/params'), 'D4': (1360, 'reservations'), 'D6': (1760, 'audit')}
    for k, (y, t) in stores.items():
        d.node('store', XS, y, SW, SH, k, [t])
    d.node('ext', XE, 600, 300, 760, 'E1', ['Huésped /', 'visitante'])
    d.node('ext', XE, 1360, 300, 130, 'E2', ['Recepción'])
    d.node('ext', XE, 1700, 300, 130, 'E3', ['Administrador'])
    d.node('ext', XE, 2040, 300, 130, 'E4', ['Superusuario'])
    d.node('svc', XR, 260, 330, 120, 'E5', ['Firebase Auth'])
    d.node('svc', XR, 600, 330, 120, 'E6', ['Geolocalización'])
    L, R = XP + PR, XS - SW / 2  # borde derecho del proceso / izquierdo del almacén
    RS = XS + SW / 2  # borde derecho del almacén
    EL = XE + 150  # borde derecho de las entidades
    # --- entidades → procesos (pares horizontales)
    for p, (ab, ba) in {'P1': ('credenciales, perfil', 'sesión iniciada'), 'P2': ('elección de cookies', 'idioma y moneda'),
                        'P3': (['fechas, huéspedes,', 'extras, código, contacto'], ['presupuesto,', 'referencia']),
                        'P4': ('registrar llegada', 'reservas del día'), 'P5': (['precio, disponibilidad,', 'promo'], 'indicadores'),
                        'P6': (['rol, bloqueo,', 'parámetros'], ['usuarios,', 'auditoría'])}.items():
        y = procs[p]
        pair(d, (EL, y), (XP - PR, y), 18, ab, ba, True, (EL + (XP - PR - EL) / 2, y - 52), (EL + (XP - PR - EL) / 2, y + 52))
    # --- P1 ↔ D1 y servicios externos
    pair(d, (L, 260), (R, 260), 16, 'crear perfil GUEST', 'rol, preferencias', True, (1010, 214), (1010, 306))
    d.edge([(XP + 40, 260 - PR + 10), (XP + 40, 120), (XR, 120), (XR, 200)], 'signUp / signIn / refresh', (1700, 96))
    d.edge([(XR - 60, 200), (XR - 60, 150), (XP + 80, 150), (XP + 80, 260 - PR + 30)], 'UID + tokens', (1250, 172))
    # --- almacenamiento local D7
    d.edge([(L - 10, 300), (900, 300), (900, 455), (R, 455)], ['refreshToken,', 'intentos'], (970, 400))
    d.edge([(L, 600), (960, 600), (960, 485), (R, 485)], ['consentimiento,', 'idioma, moneda'], (1060, 540), )
    d.edge([(L - 4, 940), (1240, 940), (1240, 500), (R, 500)], 'copia local', (1240, 760))
    # --- P2 ↔ E6 (pasa por debajo de los almacenes)
    d.edge([(L, 620), (1100, 620), (1100, 640), (XR - 165, 640)], 'lat/lon redondeadas', (1900, 615))
    d.edge([(XR - 165, 580), (1300, 580), (1300, 560), (L - 2, 560)], 'país', (1900, 556))
    # --- P3 lee catálogo y parámetros, escribe reservas
    d.edge([(R, 860), (1020, 860), (1020, 955), (L - 3, 955)], ['precio,', 'capacidad'], (1100, 820))
    d.edge([(R, 980), (L, 980)], '% descuento', (1180, 1004))
    d.edge([(R, 1100), (1060, 1100), (1060, 1005), (L - 3, 1005)], ['impuestos,', 'límites'], (1150, 1140))
    d.edge([(L - 10, 1030), (1000, 1030), (1000, 1345), (R, 1345)], 'reserva CONFIRMED', (1180, 1322))
    # --- P4 ↔ D4, P4 → D6
    d.edge([(R, 1375), (L, 1375)], 'reservas del día', (960, 1375))
    d.edge([(L - 8, 1400), (1140, 1400), (1140, 1740), (R, 1740)], 'RES_STATUS', (1230, 1716))
    # --- P5: lee D4, escribe D2, D3 (por la derecha) y D6
    d.edge([(R, 1385), (1180, 1385), (1180, 1680), (L, 1680)], 'reservas (indicadores)', (1000, 1656))
    d.edge([(L, 1720), (1100, 1720), (1100, 1760), (R, 1760)], 'ROOM_UPDATE / PROMO_*', (930, 1745))
    d.edge([(XP, 1700 + PR), (XP, 1840), (2000, 1840), (2000, 860), (RS, 860)], 'rooms actualizados', (2120, 900))
    d.edge([(XP + 50, 1700 + PR - 14), (XP + 50, 1870), (2060, 1870), (2060, 980), (RS, 980)], 'promos actualizadas', (2180, 1020))
    # --- P6: D1 (por la derecha), D5, D6
    d.edge([(XP, 2040 + PR), (XP, 2180), (2500, 2180), (2500, 345), (RS - 60, 345), (RS - 60, 260 + SH / 2)], 'role / disabled', (2420, 1300))
    d.edge([(L, 2060), (2120, 2060), (2120, 1100), (RS, 1100)], 'parámetros', (2210, 1140))
    d.edge([(L - 6, 2010), (1220, 2010), (1220, 1780), (R, 1780)], ['ROLE_CHANGE /', 'PARAMS_UPDATE'], (1400, 1985))
    d.edge([(R, 1795), (1260, 1795), (1260, 2030), (L - 2, 2030)], 'registros de auditoría', (1050, 1990))
    d.save('01b_dfd_nivel1')


nivel0(); nivel1()
print('ok')
