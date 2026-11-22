"""Edita el video de la Unidad 1: tarjetas de sección, subtítulos, música y efectos (todo generado, sin derechos de terceros).

Uso: python video_u1.py <video_original.mp4> <salida.mp4>
"""
import os, sys, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FONTS = os.path.join(ROOT, 'app', 'shared', 'src', 'commonMain', 'composeResources', 'font')
DIAG = os.path.join(ROOT, 'docs', 'diagramas')
SRC, OUT = sys.argv[1], sys.argv[2]
WORK = os.path.join(os.path.dirname(OUT), '_trabajo_video')
os.makedirs(WORK, exist_ok=True)
W, H, FPS, SR = 1440, 900, 30, 44100

TEAL, NAVY, SAND, SUN, WHITE = (10, 124, 134), (22, 49, 58), (255, 244, 226), (244, 166, 58), (255, 255, 255)


def font(name, size, bold=False):
    if name == 'serif':
        f = ImageFont.truetype(os.path.join(FONTS, 'playfair.ttf'), size)
        try: f.set_variation_by_name('Bold' if bold else 'Regular')
        except Exception: pass
        return f
    f = ImageFont.truetype(os.path.join(FONTS, 'inter.ttf'), size)
    try: f.set_variation_by_name('SemiBold' if bold else 'Regular')
    except Exception: pass
    return f


def run(args):
    subprocess.run([FF, '-v', 'error', '-y'] + args, check=True)


# ----------------------------------------------------------------------------- tarjetas
def background():
    """Degradado mar → arena con olas suaves y sol."""
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array(NAVY), np.array(TEAL)
    arr = (top * (1 - y) + bot * y)[:, :, None].repeat(W, axis=2).transpose(0, 2, 1).astype(np.uint8)
    im = Image.fromarray(arr, 'RGB')
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse([W - 260, 70, W - 120, 210], fill=SUN + (230,))
    for k, a in ((0, 40), (1, 60), (2, 90)):
        pts = [(x, H - 120 + k * 35 + 18 * np.sin(x / 120 + k)) for x in range(0, W + 20, 20)]
        d.polygon(pts + [(W, H), (0, H)], fill=SAND + (a,))
    return im


def card(name, kicker, title, lines=(), image=None, img_box=None):
    im = background()
    d = ImageDraw.Draw(im)
    d.text((110, 120), kicker.upper(), font=font('sans', 26, True), fill=SUN)
    d.text((110, 165), title, font=font('serif', 70, True), fill=WHITE)
    yy = 300
    for ln in lines:
        d.ellipse([112, yy + 14, 124, yy + 26], fill=SUN)
        d.text((145, yy), ln, font=font('sans', 32), fill=WHITE)
        yy += 62
    if image:
        pic = Image.open(image).convert('RGB')
        x0, y0, x1, y1 = img_box
        pic.thumbnail((x1 - x0, y1 - y0), Image.LANCZOS)
        px, py = x0 + (x1 - x0 - pic.width) // 2, y0 + (y1 - y0 - pic.height) // 2
        sh = Image.new('RGBA', (pic.width + 40, pic.height + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([20, 20, pic.width + 20, pic.height + 20], 18, fill=(0, 0, 0, 120))
        im.paste(sh.filter(ImageFilter.GaussianBlur(12)), (px - 14, py - 8), sh.filter(ImageFilter.GaussianBlur(12)))
        im.paste(pic, (px, py))
    path = os.path.join(WORK, name + '.png')
    im.save(path)
    return path


CARDS = [
    ('c1_intro', 6, card('c1_intro', 'Unidad 1 · Interfaz centrada en el usuario', 'Lumbre Hotel & Spa',
        ['Sistema de reservas multiplataforma: Android · iOS · Web', 'Kotlin Multiplatform + Compose · Firebase',
         'Jan Carlo Prado Anguiano · TecNM · IT Morelia'])),
    ('c2_oportunidad', 10, card('c2_oportunidad', '1 · La oportunidad', 'Reservar debería tomar un minuto',
        ['Las reservas se llevaban en hojas de cálculo, correos y llamadas',
         'Huéspedes de 8 países necesitaban su idioma y su moneda',
         'Oportunidad: una app clara que presupuesta, valida y confirma',
         'Cómo lo hicimos: diseño centrado en el usuario + nube gratuita'])),
    ('c3_usuario', 10, card('c3_usuario', '2 · Usuario objetivo', 'Conoce a Mariana, 34 años',
        ['Profesionista de Guadalajara que viaja 2–3 veces al año',
         'Experiencia tecnológica media · reserva desde el celular',
         'Necesita: precio total claro, en pesos, sin sorpresas',
         'Frustración: formularios largos y errores sin explicación'])),
    ('c4_prototipo', 11, card('c4_prototipo', '3 · Prototipo', 'Wireframes antes de programar', [],
        os.path.join(DIAG, '18_wireframes_todos.png'), (110, 270, W - 110, H - 60))),
    ('c5_flujo', 8, card('c5_flujo', '4 · User Flow', 'De la visita a la confirmación',
        ['Cookies → Inicio → Fechas → Habitación → Datos → Confirmación',
         'Validación en cada paso · presupuesto siempre visible',
         'A continuación: la aplicación funcionando'])),
]
END_CARDS = [
    ('c6_ux', 13, card('c6_ux', '5 · Principios UX aplicados', 'Por qué es fácil de usar',
        ['Retroalimentación: presupuesto en vivo, confeti y referencia',
         'Prevención de errores: validación junto al campo + sugerencias',
         'Consistencia: mismos botones y colores en web y móvil',
         'Navegación clara: pasos numerados, Atrás y cerrar siempre visibles',
         'Reconocimiento: Lumi y textos guían sin memorizar nada',
         'Accesibilidad: contraste, tema claro/oscuro y 4 idiomas'])),
    ('c7_resultado', 10, card('c7_resultado', '6 · Resultado final', 'Una app, tres plataformas',
        ['14 pantallas · reserva completa en menos de 1 minuto',
         'Cuentas, roles y datos en Firebase (plan gratuito)',
         'Web: jancarliux24.github.io/hotel-lumbre/app',
         'Código: github.com/JanCarliux24/hotel-lumbre',
         '¡Gracias!'])),
]

# Subtítulos sobre el video original (segundos del video original)
CAPTIONS = [
    (3.0, 9.0, 'Sitio web informativo · presupuesto inmediato'),
    (21.0, 27.5, 'Retroalimentación: solicitud confirmada con referencia'),
    (33.5, 40.5, 'Aviso de cookies: idioma y moneda por ubicación'),
    (42.0, 47.5, 'Catálogo de habitaciones con precios en tu moneda'),
    (48.5, 58.5, 'Reserva en 3 pasos con presupuesto siempre visible'),
    (62.5, 70.5, 'Validaciones: mensajes claros junto a cada campo'),
    (71.0, 75.0, 'Perfil: cuenta, privacidad y preferencias'),
    (78.0, 86.0, 'Vista móvil: misma app y misma nube'),
    (99.5, 106.0, 'Paso 3 en móvil: datos del huésped'),
    (108.0, 118.5, 'Prevención de errores también en el teléfono'),
]
CHIMES = [25.0]          # momento de confirmación dentro del video original
SCENE_CUTS = [2.4, 28.4, 30.8, 41.5, 75.2, 77.6]


def caption_png(i, text):
    f = font('sans', 30, True)
    tw = int(f.getlength(text))
    im = Image.new('RGBA', (tw + 90, 74), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, tw + 89, 73], 37, fill=NAVY + (225,))
    d.ellipse([22, 27, 42, 47], fill=SUN)
    d.text((58, 18), text, font=f, fill=WHITE)
    p = os.path.join(WORK, f'cap{i}.png')
    im.save(p)
    return p


# ----------------------------------------------------------------------------- audio
def env(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e


def note(f):
    return 440 * 2 ** ((f - 69) / 12)


_PLUCKS = {}


def pluck(f0):
    """Nota pulsada tipo marimba/guitarra suave (armónicos con caída exponencial)."""
    if f0 not in _PLUCKS:
        t = np.arange(int(0.7 * SR)) / SR
        y = sum(a * np.sin(2 * np.pi * f0 * h * t) * np.exp(-t * (5 + 4 * h)) for h, a in ((1, 1), (2, .35), (3, .15), (4, .07)))
        _PLUCKS[f0] = 0.05 * y * np.minimum(1, t / 0.004)
    return _PLUCKS[f0]


def music(total):
    bpm = 84; beat = 60 / bpm; bar = 4 * beat
    n = int(total * SR); out = np.zeros(n)
    rng = np.random.default_rng(7)
    prog = [(60, [60, 64, 67, 71]), (57, [57, 60, 64, 67]), (53, [53, 57, 60, 64]), (55, [55, 59, 62, 65])]
    t_bar = np.arange(int(bar * SR)) / SR
    bars = int(total / bar) + 1
    for b in range(bars):
        root, chord = prog[b % 4]
        s = int(b * bar * SR)
        seg = np.zeros(len(t_bar))
        for m in chord:  # pad cálido
            for det in (-0.12, 0.12):
                seg += 0.05 * np.sin(2 * np.pi * note(m + det) * t_bar) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t_bar))
        seg *= env(len(seg), 0.6, 0.6)
        bass = 0.18 * np.sin(2 * np.pi * note(root - 24) * t_bar) * np.exp(-t_bar * 0.9)
        seg += bass
        for k in range(8):  # arpegio pulsado (Karplus-Strong simple)
            if (b + k) % 3 == 2: continue
            ks = pluck(note(chord[k % 4] + 12))
            o = int(k * beat / 2 * SR)
            end = min(len(seg), o + len(ks)); seg[o:end] += ks[:end - o]
        for k in range(4):  # bombo suave y hi-hat
            o = int(k * beat * SR)
            if k in (0, 2):
                tk = np.arange(int(0.25 * SR)) / SR
                kick = 0.35 * np.sin(2 * np.pi * (50 + 60 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 12)
                seg[o:o + len(kick)] += kick[:len(seg) - o]
            for h in (0, 0.5):
                oh = int((k + h) * beat * SR)
                hat = rng.normal(0, 1, int(0.04 * SR)); hat = np.diff(hat, prepend=0) * np.exp(-np.arange(len(hat)) / (0.006 * SR))
                seg[oh:oh + len(hat)] += 0.025 * hat[:len(seg) - oh]
        e = min(n, s + len(seg)); out[s:e] += seg[:e - s]
    out *= env(n, 2.5, 4.0)
    return out


def whoosh(d=0.7):
    t = np.arange(int(d * SR)) / SR
    noise = np.random.default_rng(3).normal(0, 1, len(t))
    f = 300 + 2500 * np.sin(np.pi * t / d)  # barrido ascendente-descendente
    ph = np.cumsum(f) / SR
    y = noise * (0.5 + 0.5 * np.sin(2 * np.pi * ph))
    y = np.convolve(y, np.ones(12) / 12, mode='same')
    return 0.35 * y * np.sin(np.pi * t / d) ** 2


def pop():
    t = np.arange(int(0.12 * SR)) / SR
    return 0.25 * np.sin(2 * np.pi * (900 + 600 * np.exp(-t * 40)) * t) * np.exp(-t * 35)


def chime():
    t = np.arange(int(1.6 * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((1046.5, .5), (1568, .3), (2093, .2), (2637, .1)))
    return 0.22 * y * np.exp(-t * 3)


def add(buf, clip, at):
    s = int(at * SR); e = min(len(buf), s + len(clip))
    if s < len(buf): buf[s:e] += clip[:e - s]


def write_wav(path, x):
    x = x / max(1e-6, np.max(np.abs(x))) * 0.89
    st = np.stack([x, x], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


# ----------------------------------------------------------------------------- montaje
def card_clip(png, dur, name, zoom=False):
    out = os.path.join(WORK, name + '.mp4')
    z = ("zoompan=z='min(1+0.0009*on,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=%d:s=%dx%d:fps=%d," % (dur * FPS, W, H, FPS)) if zoom else ''
    vf = f"{z}scale={W}:{H},fps={FPS},fade=t=in:st=0:d=0.6,fade=t=out:st={dur - 0.6}:d=0.6,format=yuv420p"
    inp = ['-i', png] if zoom else ['-loop', '1', '-t', str(dur), '-i', png]  # zoompan genera sus propios cuadros
    run(inp + ['-vf', vf, '-t', str(dur), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', out])
    return out


def main_clip():
    out = os.path.join(WORK, 'main.mp4')
    if os.path.exists(out) and os.environ.get('REUSAR_MAIN'):
        return out
    args = ['-i', SRC]
    caps = [caption_png(i, c[2]) for i, c in enumerate(CAPTIONS)]
    for p in caps: args += ['-loop', '1', '-i', p]
    fc = [f"[0:v]scale={W}:{H},fps={FPS},setpts=PTS-STARTPTS[v0]"]
    last = 'v0'
    for i, (a, b, _) in enumerate(CAPTIONS):
        fc.append(f"[{i + 1}:v]format=rgba,fade=t=in:st={a}:d=0.4:alpha=1,fade=t=out:st={b - 0.4}:d=0.4:alpha=1[c{i}]")
        fc.append(f"[{last}][c{i}]overlay=x=(W-w)/2:y=H-h-48:enable='between(t,{a},{b})':shortest=1[v{i + 1}]")
        last = f'v{i + 1}'
    fc.append(f"[{last}]format=yuv420p[vout]")
    run(args + ['-filter_complex', ';'.join(fc), '-map', '[vout]', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', out])
    return out


def duration(path):
    r = subprocess.run([FF, '-i', path], capture_output=True, text=True).stderr
    h, m, s = r.split('Duration: ')[1].split(',')[0].split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def build():
    clips, marks = [], []
    t = 0.0
    for name, dur, png in CARDS:
        clips.append(card_clip(png, dur, name, zoom=(name == 'c4_prototipo'))); marks.append(('card', t)); t += dur
    main = main_clip(); main_start = t; md = duration(main); clips.append(main); marks.append(('card', t)); t += md
    for name, dur, png in END_CARDS:
        clips.append(card_clip(png, dur, name)); marks.append(('card', t)); t += dur
    total = t
    lst = os.path.join(WORK, 'lista.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for c in clips: f.write(f"file '{c.replace(os.sep, '/')}'\n")
    video = os.path.join(WORK, 'video_sin_audio.mp4')
    run(['-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', video])

    audio = music(total)
    for _, at in marks: add(audio, whoosh(), max(0, at - 0.35))
    for c in SCENE_CUTS: add(audio, whoosh(0.5) * 0.6, main_start + c - 0.25)
    for a, _, _ in CAPTIONS: add(audio, pop(), main_start + a)
    for c in CHIMES: add(audio, chime(), main_start + c)
    add(audio, chime(), t - END_CARDS[-1][1] + 1.0)
    wav = os.path.join(WORK, 'audio.wav'); write_wav(wav, audio)
    run(['-i', video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         '-shortest', '-movflags', '+faststart', OUT])
    print(f'listo: {OUT} · {total:.1f} s')


if __name__ == '__main__':
    build()
