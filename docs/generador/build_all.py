"""Genera los 13 entregables en docs/entregables y el script SQL en docs/bd."""
import os
import u2_docs, bd_docs
from docgen import ROOT

os.makedirs(os.path.join(ROOT, 'docs', 'bd'), exist_ok=True)
with open(os.path.join(ROOT, 'docs', 'bd', 'lumbre.sql'), 'w', encoding='utf-8') as f:
    f.write('-- Lumbre Hotel & Spa: modelo relacional normalizado (PostgreSQL)\n' + bd_docs.DDL + '\n')
for fn in u2_docs.ALL + bd_docs.ALL:
    print(fn())
