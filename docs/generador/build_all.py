"""Genera los 16 entregables (U1: 3 · U2 librerías: 6 · U2 bases de datos: 7) y el script SQL."""
import os
import u1_docs, u2_docs, bd_docs
from docgen import ROOT

os.makedirs(os.path.join(ROOT, 'docs', 'bd'), exist_ok=True)
with open(os.path.join(ROOT, 'docs', 'bd', 'lumbre.sql'), 'w', encoding='utf-8') as f:
    f.write('-- Lumbre Hotel & Spa: modelo relacional normalizado (PostgreSQL)\n' + bd_docs.DDL + '\n')
for fn in u1_docs.ALL + u2_docs.ALL + bd_docs.ALL:
    print(fn())
