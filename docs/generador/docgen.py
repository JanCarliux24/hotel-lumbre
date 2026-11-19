"""Generador de documentos .docx para los entregables (luego se convierten a Google Docs)."""
import os
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DIAG = os.path.join(ROOT, 'docs', 'diagramas')
SHOTS = os.path.join(ROOT, 'docs', 'capturas')
OUT = os.path.join(ROOT, 'docs', 'entregables')
os.makedirs(OUT, exist_ok=True)

TEAL = RGBColor(0x0A, 0x7C, 0x86)
NAVY = RGBColor(0x16, 0x31, 0x3A)
GOLD = RGBColor(0xB8, 0x7A, 0x1E)
GREY = RGBColor(0x5B, 0x6E, 0x73)

AUTOR = 'Jan Carlo Prado Anguiano'
REPO = 'https://github.com/JanCarliux24/hotel-lumbre'
WEB = 'https://jancarliux24.github.io/hotel-lumbre/'
APPWEB = 'https://jancarliux24.github.io/hotel-lumbre/app/'
APK = 'https://jancarliux24.github.io/hotel-lumbre/app/lumbre.apk'


def _shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


class Doc:
    def __init__(self, filename, unidad, entregable_num, titulo, subtitulo):
        self.filename = filename
        self.d = Document()
        sec = self.d.sections[0]
        sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)  # carta
        for side in ('left_margin', 'right_margin'):
            setattr(sec, side, Cm(2.3))
        sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.2)
        st = self.d.styles
        st['Normal'].font.name = 'Calibri'; st['Normal'].font.size = Pt(11)
        st['Normal'].paragraph_format.space_after = Pt(6)
        st['Normal'].paragraph_format.line_spacing = 1.15
        for lvl, size, color in ((1, 18, TEAL), (2, 14, NAVY), (3, 12, GOLD)):
            h = st[f'Heading {lvl}']
            h.font.name = 'Calibri'; h.font.size = Pt(size); h.font.bold = True; h.font.color.rgb = color
            h.paragraph_format.space_before = Pt(14 if lvl == 1 else 10); h.paragraph_format.space_after = Pt(6)
            h.paragraph_format.keep_with_next = True
        self._fig = 0
        self._tab = 0
        self._cover(unidad, entregable_num, titulo, subtitulo)
        self._footer(f'{titulo} · Lumbre Hotel & Spa')

    # ---------- Portada y pie ----------
    def _cover(self, unidad, num, titulo, subtitulo):
        d = self.d
        for text, size, bold, color in (
            ('Tecnológico Nacional de México', 20, True, NAVY),
            ('Instituto Tecnológico de Morelia', 16, True, NAVY),
        ):
            p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.font.color.rgb = color
        d.add_paragraph()
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(unidad); r.font.size = Pt(13); r.font.color.rgb = GREY
        d.add_paragraph()
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(num.upper()); r.font.size = Pt(13); r.bold = True; r.font.color.rgb = GOLD
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(titulo); r.font.size = Pt(26); r.bold = True; r.font.color.rgb = TEAL
        p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(subtitulo); r.font.size = Pt(13); r.italic = True; r.font.color.rgb = NAVY
        d.add_paragraph(); d.add_paragraph()
        meta = [
            ('Proyecto', 'Lumbre Hotel & Spa — sistema de reservas multiplataforma (Android, iOS y web)'),
            ('Integrante(s)', AUTOR + ' (añadir el resto del equipo si aplica)'),
            ('Repositorio', REPO),
            ('Aplicación web', APPWEB),
            ('Fecha', 'Noviembre de 2026'),
        ]
        t = d.add_table(rows=0, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for k, v in meta:
            row = t.add_row().cells
            row[0].text = k; row[1].text = v
            row[0].paragraphs[0].runs[0].bold = True
            _shade(row[0], 'E6F6FA')
            row[0].width = Cm(4); row[1].width = Cm(12)
        p = d.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)

    def _footer(self, text):
        p = self.d.sections[0].footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text + ' · Página '); r.font.size = Pt(9); r.font.color.rgb = GREY
        run = p.add_run()
        for tag, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
            if tag:
                el = OxmlElement('w:fldChar'); el.set(qn('w:fldCharType'), tag); run._r.append(el)
            else:
                it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = txt; run._r.append(it)
        run.font.size = Pt(9)

    # ---------- Bloques ----------
    def toc(self, items):
        self.h1('Contenido')
        for i, it in enumerate(items, 1):
            p = self.d.add_paragraph(f'{i}. {it}')
            p.paragraph_format.space_after = Pt(2)
        self.page_break()

    def h1(self, t): self.d.add_heading(t, 1)
    def h2(self, t): self.d.add_heading(t, 2)
    def h3(self, t): self.d.add_heading(t, 3)

    def p(self, text, bold_prefix=None, italic=False):
        par = self.d.add_paragraph()
        if bold_prefix:
            r = par.add_run(bold_prefix + ' '); r.bold = True
        r = par.add_run(text); r.italic = italic
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return par

    def bullets(self, items, numbered=False):
        style = 'List Number' if numbered else 'List Bullet'
        for it in items:
            par = self.d.add_paragraph(style=style)
            if isinstance(it, tuple):
                r = par.add_run(it[0] + ': '); r.bold = True
                par.add_run(it[1])
            else:
                par.add_run(it)

    def note(self, text, title='Nota'):
        t = self.d.add_table(rows=1, cols=1)
        c = t.rows[0].cells[0]; _shade(c, 'FFF4E2')
        c.text = ''
        par = c.paragraphs[0]
        r = par.add_run(title + '. '); r.bold = True; r.font.color.rgb = GOLD
        par.add_run(text)
        self.d.add_paragraph()

    def code(self, text, caption=None):
        t = self.d.add_table(rows=1, cols=1)
        c = t.rows[0].cells[0]; _shade(c, 'F3F6F7')
        c.text = ''
        par = c.paragraphs[0]
        r = par.add_run(text.strip('\n')); r.font.name = 'Consolas'; r.font.size = Pt(9)
        r._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')
        if caption:
            cp = self.d.add_paragraph(); rr = cp.add_run(caption); rr.italic = True; rr.font.size = Pt(9); rr.font.color.rgb = GREY
        else:
            self.d.add_paragraph()

    def table(self, header, rows, widths=None, caption=None, font=9.5):
        self._tab += 1
        if caption:
            cp = self.d.add_paragraph(); r = cp.add_run(f'Tabla {self._tab}. {caption}'); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = NAVY
        t = self.d.add_table(rows=1, cols=len(header))
        t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, h in enumerate(header):
            c = t.rows[0].cells[i]; c.text = ''
            r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(font); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            _shade(c, '0A7C86')
        for ri, row in enumerate(rows):
            cells = t.add_row().cells
            for i, v in enumerate(row):
                cells[i].text = ''
                r = cells[i].paragraphs[0].add_run(str(v)); r.font.size = Pt(font)
                if ri % 2 == 1: _shade(cells[i], 'F6FBFC')
        if widths:
            for row in t.rows:
                for i, w in enumerate(widths):
                    row.cells[i].width = Cm(w)
        self.d.add_paragraph()
        return t

    def image(self, path, caption, width_cm=16.5):
        if not os.path.exists(path):
            self.note(f'Imagen no disponible: {os.path.basename(path)}', 'Aviso'); return
        self._fig += 1
        par = self.d.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.add_run().add_picture(path, width=Cm(width_cm))
        cp = self.d.add_paragraph(); cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cp.add_run(f'Figura {self._fig}. {caption}'); r.italic = True; r.font.size = Pt(9.5); r.font.color.rgb = GREY

    def diagram(self, name, caption, width_cm=16.5):
        self.image(os.path.join(DIAG, name), caption, width_cm)

    def shot(self, name, caption, width_cm=15):
        self.image(os.path.join(SHOTS, name), caption, width_cm)

    def page_break(self):
        self.d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def save(self):
        path = os.path.join(OUT, self.filename)
        self.d.save(path)
        return path
