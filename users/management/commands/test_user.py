from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания тестового пользователя в проекте"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email="test@example.com",
            is_active=True,
        )
        user.set_password("test")
        user.save()
