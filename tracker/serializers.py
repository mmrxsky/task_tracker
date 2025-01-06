from rest_framework import serializers

from tracker.models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника"""

    class Meta:
        model = Employee
        fields = ('full_name', 'position',)


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи"""

    class Meta:
        model = Task
        fields = '__all__'