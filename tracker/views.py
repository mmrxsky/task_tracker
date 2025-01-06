from django.db.models import Q
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from tracker.models import Employee, Task
from tracker.serializers import (
    EmployeeSerializer,
    TaskSerializer,
    EmployeeTrackSerializer,
    ImportantTaskSerializer,
)
from users.permissions import IsStaff


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудников"""

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def perform_create(self, serializer):
        new_employee = serializer.save
        new_employee.user = self.request.user
        new_employee.save()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (
                IsAuthenticated,
                IsStaff,
            )
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()


class TaskListAPIView(ListAPIView):
    """Класс для просмотра списка всех задач"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskRetrieveAPIView(RetrieveAPIView):
    """Класс для просмотра конкретной задачи"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskCreateAPIView(CreateAPIView):
    """Класс для создания новой задачи"""

    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsStaff)

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.user = self.request.user
        new_task.save()


class TaskUpdateAPIView(UpdateAPIView):
    """Класс для изменения конкретной задачи"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsStaff)


class TaskDeleteAPIView(DestroyAPIView):
    """Класс для удаления конкретной задачи"""

    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, IsStaff)


class EmployeeTrackAPIView(ListAPIView):
    """Класс для вывода списка активных задач сотрудника"""

    serializer_class = EmployeeTrackSerializer
    queryset = Employee.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ["active_task_count"]


class ImportantTasksAPIView(ListAPIView):
    """Класс для вывода списка важных задач не взятых в работу, но от которых не зависят другие задачи взятые в
    работу"""

    serializer_class = ImportantTaskSerializer

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(
            Q(is_active=False)
            & (
                Q(parent_task__is_active=True)
                | Q(parent_task__parent_task__is_active=True)
                | Q(parent_task__parent_task__parent_task__is_active=True)
            )
        )
