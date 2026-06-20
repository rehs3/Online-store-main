from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()


User = get_user_model()

try:
    # Verifica se o usuário já existe
    if User.objects.filter(email='regina@gmail.com').exists():
        print('❌ Usuário com email "regina@gmail.com" já existe.')
    else:
        # Cria o superuser
        user = User.objects.create_superuser(
            email='regina@gmail.com',
            user_name='regina',
            password='ufc123',
            is_staff=True,
            is_superuser=True
        )
        print(f'✅ Superusuário "regina" criado com sucesso!')
        print(f'   Email: regina@gmail.com')
        print(f'   Senha: ufc123')
except Exception as e:
    print(f'❌ Erro ao criar usuário: {str(e)}')
