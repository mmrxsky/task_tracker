import os
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания админа"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@example.com',
            first_name='admin',
            last_name='admin',
            is_staff=True,
            is_superuser=True,
        )
        user.set_password('123qwe')
        user.save()