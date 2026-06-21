import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

from catalog.models import Product, Category

# Mapear categorias para padrões de arquivo que representam imagens adequadas
mapping = {
    'Óculos': ['sunglass', 'glass', 'prada', 'gucci', 'ray', 'oakley'],
    'Joias': ['ring', 'necklace', 'brinc', 'pulseira', 'diamond', 'brazalete', 'anel', 'col'],
    'Roupas': ['shirt', 'dress', 'jacket', 'jeans', 'pants', 'tshirt', 'trousers']
}

media_dir = os.path.join(os.getcwd(), 'media', 'product_image', 'product_photo')
if not os.path.exists(media_dir):
    print('Pasta de imagens não encontrada:', media_dir)
    raise SystemExit(1)

files = [f for f in os.listdir(media_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# função que encontra arquivo por palavra-chave
def find_image_for_category(cat_key):
    keys = mapping.get(cat_key, [])
    for k in keys:
        for f in files:
            if k.lower() in f.lower():
                return os.path.join('product_image', 'product_photo', f)
    return None

for cat_title in ['Óculos', 'Joias', 'Roupas']:
    try:
        cat = Category.objects.get(title=cat_title)
    except Category.DoesNotExist:
        print('Categoria não encontrada:', cat_title)
        continue

    img = find_image_for_category(cat_title)
    if not img:
        print('Nenhuma imagem encontrada para categoria', cat_title)
        continue

    products = Product.objects.filter(category=cat)
    if not products.exists():
        print('Nenhum produto na categoria', cat_title)
        continue

    for p in products:
        p.image = img
        p.save()
        print('Atualizado', p.title, '->', img)

print('Atualização concluída.')
