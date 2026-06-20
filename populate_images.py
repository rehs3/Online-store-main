from catalog.models import Product, Gallery
from django.core.files import File
from pathlib import Path
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()


# Caminho base da mídia
media_base = Path('media/product_image/photo/Rolex/Rolex Air King')

# Atualizar o produto Rolex com a primeira imagem encontrada
rolex_product = Product.objects.filter(title='Rolex').first()
if rolex_product and media_base.exists():
    images = list(media_base.glob('*.jpg'))
    if images:
        # Usar a primeira imagem como imagem principal
        main_image_path = images[0]
        relative_path = f'product_image/photo/Rolex/Rolex Air King/{main_image_path.name}'

        rolex_product.image = relative_path
        rolex_product.save()
        print(
            f'✅ Imagem principal do Rolex atualizada: {main_image_path.name}')

        # Adicionar todas as imagens como galeria
        for img_path in images:
            relative_path = f'product_image/photo/Rolex/Rolex Air King/{img_path.name}'

            # Verificar se já existe
            if not Gallery.objects.filter(product=rolex_product, image=relative_path).exists():
                Gallery.objects.create(
                    product=rolex_product,
                    image=relative_path
                )
                print(f'✅ Imagem adicionada à galeria: {img_path.name}')

# Tentar encontrar e adicionar imagens para outros produtos genéricos
for product in Product.objects.all():
    if not product.image or 'default' in product.image.name:
        # Tentar usar uma imagem da pasta Rolex para todos
        images = list(media_base.glob('*.jpg'))
        if images:
            relative_path = f'product_image/photo/Rolex/Rolex Air King/{images[0].name}'
            product.image = relative_path
            product.save()
            print(f'✅ Imagem adicionada ao produto: {product.title}')

print(
    f'\n✅ Total de produtos com imagens: {Product.objects.exclude(image__contains="default").count()}')
print(f'✅ Total de imagens na galeria: {Gallery.objects.count()}')
