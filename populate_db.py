from catalog.models import Category, Product
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()


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

print('✅ Dados de teste criados com sucesso!')
print(f'Categorias: {Category.objects.count()}')
print(f'Produtos: {Product.objects.count()}')
