from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Класс для создания пользователя"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс для просмотра, изменения и удаления пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
