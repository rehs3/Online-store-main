import os
import django

# Ensure DJANGO_SETTINGS_MODULE is set before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()
from catalog.models import Category, Product


# Criar Categorias
cat1, _ = Category.objects.get_or_create(title='Relógios')
cat2, _ = Category.objects.get_or_create(title='Óculos')
cat3, _ = Category.objects.get_or_create(title='Joias')

# Criar Produtos
Product.objects.get_or_create(
    title='Rolex',
    defaults={
        'category': cat1,
        'description': 'Relógio de luxo suíço de alta precisão',
        'price': 5000,
        'quantity': 10
    }
)

Product.objects.get_or_create(
    title='Omega',
    defaults={
        'category': cat1,
        'description': 'Relógio automático de qualidade premium',
        'price': 3500,
        'quantity': 15
    }
)

Product.objects.get_or_create(
    title='Ray Ban',
    defaults={
        'category': cat2,
        'description': 'Óculos de sol clássicos e modernos',
        'price': 150,
        'quantity': 50
    }
)

Product.objects.get_or_create(
    title='Pulseira Ouro',
    defaults={
        'category': cat3,
        'description': 'Pulseira de ouro 18 quilates',
        'price': 800,
        'quantity': 8
    }
)

Product.objects.get_or_create(
    title='Colar Diamante',
    defaults={
        'category': cat3,
        'description': 'Colar com diamante natural',
        'price': 2000,
        'quantity': 5
    }
)

Product.objects.get_or_create(
    title='Seiko',
    defaults={
        'category': cat1,
        'description': 'Relógio automático japonês de confiança',
        'price': 600,
        'quantity': 20
    }
)

# Produtos adicionais com imagens diferentes
Product.objects.get_or_create(
    title='Tissot PRX',
    defaults={
        'category': cat1,
        'description': 'Relógio Tissot PRX elegante e acessível',
        'price': 450,
        'quantity': 25,
        'image': 'product_image/product_photo/new-rolex-air-king-watch.jpg'
    }
)

Product.objects.get_or_create(
    title='Gucci Sunglasses',
    defaults={
        'category': cat2,
        'description': 'Óculos de sol Gucci com estilo moderno',
        'price': 220,
        'quantity': 30,
        'image': 'product_image/product_photo/Aquanaut_5168.jpg'
    }
)

Product.objects.get_or_create(
    title='Oakley Sport',
    defaults={
        'category': cat2,
        'description': 'Óculos Oakley para esportes',
        'price': 180,
        'quantity': 40,
        'image': 'product_image/product_photo/Type_XXI_3jpg.jpg'
    }
)

Product.objects.get_or_create(
    title='Brinco Ouro',
    defaults={
        'category': cat3,
        'description': 'Brinco em ouro 18k elegante',
        'price': 350,
        'quantity': 12,
        'image': 'product_image/product_photo/Rolex_Cellini_Date_2.jpg'
    }
)

Product.objects.get_or_create(
    title='Anel Solitário',
    defaults={
        'category': cat3,
        'description': 'Anel com pedra preciosa',
        'price': 1200,
        'quantity': 6,
        'image': 'product_image/product_photo/Tradition_3.jpg'
    }
)

print('✅ Dados de teste criados com sucesso!')

# Adicionar mais produtos automaticamente usando imagens únicas da pasta media
images_dir = os.path.join(os.path.dirname(__file__), 'media', 'product_image', 'product_photo')
if not os.path.exists(images_dir):
    # tentar caminho relativo ao BASE_DIR
    images_dir = os.path.join(os.getcwd(), 'media', 'product_image', 'product_photo')

available_images = []
if os.path.exists(images_dir):
    for f in os.listdir(images_dir):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            available_images.append(os.path.join('product_image', 'product_photo', f))

titles = [
    'Audemars Piguet', 'Patek Philippe', 'Tissot', 'Casio', 'Gucci Sunglasses',
    'Prada Sunglasses', 'Bulgari Ring', 'Swarovski Necklace', 'Citizen', 'Hamilton',
    'Fossil', 'Tom Ford Sunglasses', 'Mido', 'Longines', 'Hublot'
]

idx = 0
for title in titles:
    if Product.objects.filter(title=title).exists():
        continue
    img = None
    if available_images:
        img = available_images[idx % len(available_images)]
        idx += 1

    # assign category round-robin among existing categories
    cats = list(Category.objects.all())
    category = cats[idx % len(cats)] if cats else cat1

    defaults = {
        'category': category,
        'description': f'Produto {title} excelente qualidade.',
        'price': 100 + (idx * 10) % 1000,
        'quantity': 20
    }
    if img:
        defaults['image'] = img

    Product.objects.get_or_create(title=title, defaults=defaults)

print('✅ Dados de teste criados com sucesso!')
print(f'Categorias: {Category.objects.count()}')
print(f'Produtos: {Product.objects.count()}')
