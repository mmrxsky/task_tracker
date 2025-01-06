from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from tracker.models import Employee, Task
from tracker.serializers import EmployeeSerializer, TaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet для сотрудников"""
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


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


class TaskUpdateAPIView(UpdateAPIView):
    """Класс для изменения конкретной задачи"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class TaskDeleteAPIView(DestroyAPIView):
    """Класс для удаления конкретной задачи"""

    queryset = Task.objects.all()
