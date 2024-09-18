import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания менеджера проекта"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email=os.getenv('MANAGER_EMAIL'),
            is_active=True,
            is_staff=True,
        )
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
