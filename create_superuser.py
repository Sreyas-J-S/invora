import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoice_system_management.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'password123'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
