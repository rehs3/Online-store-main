from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

User = get_user_model()

SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ufc123')

try:
    if User.objects.filter(email='regina@gmail.com').exists():
        print('❌ Usuário com email "regina@gmail.com" já existe.')
    else:
        user = User.objects.create_superuser(
            email='regina@gmail.com',
            user_name='regina',
            password=SUPERUSER_PASSWORD,
            is_staff=True,
            is_superuser=True
        )
        print('✅ Superusuário "regina" criado com sucesso!')
        print('   Email: regina@gmail.com')
        print('   Senha: [Definida via variável de ambiente ou valor padrão]')
except Exception as e:
    print(f'❌ Erro ao criar usuário: {str(e)}')
