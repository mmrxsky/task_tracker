from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания модератора проекта"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email="moderator@example.com",
            is_active=True,
            is_staff=True,
        )
        user.set_password("qwe123")
        user.save()
