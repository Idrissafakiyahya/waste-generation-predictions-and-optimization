import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_project.settings')

import django
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = 'Admin123!'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Created superuser:', username)
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print('Superuser password reset for:', username)

print('Login with username:', username, 'password:', password)
