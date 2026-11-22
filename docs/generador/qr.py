"""Códigos QR de descarga: APK (Android) y app web. Genera QR individuales y una tarjeta con ambos."""
import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'capturas')
FONT = os.path.join(ROOT, 'app', 'shared', 'src', 'commonMain', 'composeResources', 'font', 'inter.ttf')
SERIF = os.path.join(ROOT, 'app', 'shared', 'src', 'commonMain', 'composeResources', 'font', 'playfair.ttf')
LINKS = [('qr_apk', 'Descarga la app Android (APK)', 'https://jancarliux24.github.io/hotel-lumbre/app/lumbre.apk'),
         ('qr_web', 'Abre la app web', 'https://jancarliux24.github.io/hotel-lumbre/app/')]
NAVY, TEAL, SUN = (22, 49, 58), (10, 124, 134), (244, 166, 58)


def f(path, size, bold=False):
    ft = ImageFont.truetype(path, size)
    try: ft.set_variation_by_name('Bold' if bold else 'Regular')
    except Exception: pass
    return ft


def make(url):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=16, border=2)
    q.add_data(url); q.make(fit=True)
    return q.make_image(fill_color=NAVY, back_color='white').convert('RGB')


imgs = []
for name, title, url in LINKS:
    im = make(url).resize((720, 720), Image.NEAREST)
    im.save(os.path.join(OUT, name + '.png'))
    imgs.append((im, title, url))

# tarjeta con ambos códigos
W, H = 1800, 1150
card = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(card)
d.rectangle([0, 0, W, 150], fill=TEAL)
d.text((W / 2, 75), 'Lumbre Hotel & Spa · descarga y prueba la app', font=f(SERIF, 58, True), fill='white', anchor='mm')
for i, (im, title, url) in enumerate(imgs):
    x = 120 + i * 840
    d.rounded_rectangle([x - 20, 200, x + 740, 1100], 36, outline=(220, 232, 234), width=4)
    card.paste(im, (x + 20, 230))
    d.text((x + 360, 985), title, font=f(FONT, 40, True), fill=NAVY, anchor='mm')
    d.text((x + 360, 1045), url.replace('https://', ''), font=f(FONT, 26), fill=TEAL, anchor='mm')
card.save(os.path.join(OUT, 'qr_descargas.png'))
print('ok')
