# create_superuser.py

import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='SuperUser',
        email='SuperUser@example.com',
        password='SuperUser'
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
