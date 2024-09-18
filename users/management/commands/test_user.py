import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания тестового пользователя в проекте"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email=os.getenv('TEST_USER_EMAIL'),
            is_active=True,
        )
        user.set_password(os.getenv('TEST_USER_PASSWORD'))
        user.save()
