import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','clothing_store.settings')
import django
django.setup()
from account.models import CustomUser
admins = list(CustomUser.objects.filter(is_superuser=True).values('id','email','user_name'))
print(admins)
