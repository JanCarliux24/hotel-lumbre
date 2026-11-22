"""Convierte SVG a PNG con Chrome sin interfaz (Playwright): mismo dibujo que el vectorial.
uso: python raster_svg.py archivo.svg [...]   (escala 1.5 por defecto)"""
import sys, os, re
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True)
    for f in sys.argv[1:]:
        svg = open(f, encoding='utf-8').read()
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg) or re.search(r'width="([\d.]+)px" height="([\d.]+)px"', svg)
        w, h = int(float(m.group(1))), int(float(m.group(2)))
        scale = float(os.environ.get('ESCALA', '1.5'))
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
        pg.set_content('<html><body style="margin:0;background:#fff">' + svg + '</body></html>')
        pg.wait_for_timeout(300)
        pg.locator('svg').first.screenshot(path=f[:-4] + '.png')
        pg.close()
        print('png', os.path.basename(f[:-4]) + '.png', w, h)
    b.close()
