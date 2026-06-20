from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()


User = get_user_model()

try:
    user = User.objects.get(email='regina@gmail.com')
    user_name = user.user_name
    user.delete()
    print(
        f'✅ Usuário "{user_name}" com email "regina@gmail.com" foi excluído com sucesso!')
except User.DoesNotExist:
    print('❌ Usuário com email "regina@gmail.com" não encontrado.')
except Exception as e:
    print(f'❌ Erro ao excluir usuário: {str(e)}')
