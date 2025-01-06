from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from tracker.models import Employee, Task
from tracker.serializers import EmployeeSerializer, TaskSerializer
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
        if self.action in ['create', 'destroy']:
            self.permission_classes = (
                IsAuthenticated,
                IsStaff,
            )
        elif self.action in ['update', 'retrieve']:
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
