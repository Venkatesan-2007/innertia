#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innertia.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.get(username='student001')
u.set_password('abc123')
u.save()
print('✓ Password updated for student001 to abc123')
