from catalog.models import Product, Gallery
from pathlib import Path
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

media_base = Path('media/product_image/photo/Rolex/Rolex Air King')

rolex_product = Product.objects.filter(title='Rolex').first()
if rolex_product and media_base.exists():
    images = list(media_base.glob('*.jpg'))
    if images:
        main_image_path = images[0]
        relative_path = f'product_image/photo/Rolex/Rolex Air King/{main_image_path.name}'

        rolex_product.image = relative_path
        rolex_product.save()
        print(
            f'✅ Imagem principal do Rolex atualizada: {main_image_path.name}')

        for img_path in images:
            relative_path = f'product_image/photo/Rolex/Rolex Air King/{img_path.name}'

            if not Gallery.objects.filter(product=rolex_product, image=relative_path).exists():
                Gallery.objects.create(
                    product=rolex_product,
                    image=relative_path
                )
                print(f'✅ Imagem adicionada à galeria: {img_path.name}')

for product in Product.objects.prefetch_related('gallery_set').all():
    if not product.image or 'default' in product.image.name:
        images = list(media_base.glob('*.jpg'))
        if images:
            relative_path = f'product_image/photo/Rolex/Rolex Air King/{images[0].name}'
            product.image = relative_path
            product.save()
            print(f'✅ Imagem adicionada ao produto: {product.title}')

print(
    f'\n✅ Total de produtos com imagens: {Product.objects.exclude(image__contains="default").count()}')
print(f'✅ Total de imagens na galeria: {Gallery.objects.count()}')
