import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','clothing_store.settings')
django.setup()
from catalog.models import Product

media_folder = os.path.join('media','product_image','product_photo')
if not os.path.exists(media_folder):
    print('Pasta de imagens não encontrada:', media_folder)
    raise SystemExit(1)

files = [f for f in os.listdir(media_folder) if f.lower().endswith(('.png','.jpg','.jpeg','.gif'))]
if not files:
    print('Nenhuma imagem encontrada em', media_folder)
    raise SystemExit(1)

products = list(Product.objects.all())
if not products:
    print('Nenhum produto encontrado no banco.')
    raise SystemExit(1)

assigned = []
for i, p in enumerate(products):
    img = files[i % len(files)]
    rel = os.path.join('product_image','product_photo', img)
    p.image = rel
    p.save()
    assigned.append((p.title, rel))

print('Imagens atribuídas:')
for title, path in assigned:
    print('-', title, '->', path)
print('Total produtos:', len(assigned))
