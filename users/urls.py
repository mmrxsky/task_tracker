from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserDetailAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("profile/<int:pk>/", UserDetailAPIView.as_view(), name="profile"),
]