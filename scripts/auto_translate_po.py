import polib
from googletrans import Translator
from pathlib import Path

po_path = Path('locale/pt_BR/LC_MESSAGES/django.po')
if not po_path.exists():
    print('Arquivo .po não encontrado:', po_path)
    raise SystemExit(1)

po = polib.pofile(str(po_path))
translator = Translator()
changed = 0

for entry in po:
    # Skip entries that already translated
    if entry.obsolete:
        continue
    if entry.msgstr:
        continue

    # Handle plural
    if entry.msgid_plural:
        # translate singular and plural separately
        try:
            trans_sing = translator.translate(entry.msgid, dest='pt').text
            trans_plur = translator.translate(entry.msgid_plural, dest='pt').text
        except Exception as e:
            print('Erro ao traduzir:', entry.msgid, e)
            continue
        entry.msgstr_plural[0] = trans_sing
        # for simplicity set plural form same as plural translation
        entry.msgstr_plural[1] = trans_plur
        changed += 1
    else:
        try:
            translated = translator.translate(entry.msgid, dest='pt').text
        except Exception as e:
            print('Erro ao traduzir:', entry.msgid, e)
            continue
        entry.msgstr = translated
        changed += 1

po.save()
print(f'Traduziu {changed} entradas em {po_path}')
