import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innertia.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

users = User.objects.filter(role__in=['faculty', 'student'])
print("\n=== Faculty and Student Users ===")
for u in users:
    print(f'{u.username:15} - role: {u.role:8} | is_active: {str(u.is_active):5} | id: {u.id}')

print("\n=== All Users ===")
all_users = User.objects.all()
for u in all_users:
    print(f'{u.username:15} - role: {u.role:8} | is_active: {str(u.is_active):5} | id: {u.id}')
