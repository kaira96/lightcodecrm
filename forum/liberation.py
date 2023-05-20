
import os
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
from django.conf import settings

if not settings.configured:
    django.setup()

from forum.models import AccessRights


def user_liberation():
    today = date.today()
    banned_users = AccessRights.objects.filter(end_date__lte=today)

    for banned_user in banned_users:
        banned_user.user.is_banned = 1
        banned_user.user.save()
    banned_users.delete()


user_liberation()


