import polib
from pathlib import Path
import os

site_packages = Path('.venv/Lib/site-packages')
if not site_packages.exists():
    print('site-packages not found at', site_packages)
    raise SystemExit(1)

po_files = list(site_packages.glob('**/pt_BR/LC_MESSAGES/django.po'))
print('Encontrei', len(po_files), 'arquivos de tradução em site-packages')

mapping = {}
plural_mapping = {}
for f in po_files:
    try:
        p = polib.pofile(str(f))
    except Exception as e:
        print('Erro lendo', f, e)
        continue
    for entry in p:
        if entry.obsolete:
            continue
        if entry.msgstr:
            mapping[entry.msgid] = entry.msgstr
        elif entry.msgstr_plural:
            plural_mapping[entry.msgid] = entry.msgstr_plural

# Load project po
proj_po_path = Path('locale/pt_BR/LC_MESSAGES/django.po')
if not proj_po_path.exists():
    print('Arquivo de projeto não encontrado:', proj_po_path)
    raise SystemExit(1)

proj = polib.pofile(str(proj_po_path))
filled = 0
for entry in proj:
    if entry.obsolete:
        continue
    if entry.msgstr:
        continue
    if entry.msgid in mapping:
        entry.msgstr = mapping[entry.msgid]
        filled += 1
    elif entry.msgid in plural_mapping:
        # try to set plural forms
        entry.msgstr_plural = plural_mapping[entry.msgid]
        filled += 1

proj.save()
print(f'Preenchi {filled} entradas no {proj_po_path}')
