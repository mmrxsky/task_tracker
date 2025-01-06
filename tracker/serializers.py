from rest_framework import serializers

from tracker.models import Employee, Task
from tracker.validators import RelatedTaskValid, NestingOfTaskValid, StatusTaskValid


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
        validators = [
            RelatedTaskValid(field='parent_task'),
            NestingOfTaskValid(field='parent_task'),
            StatusTaskValid(field='status'),
        ]

class EmployeeTrackSerializer(serializers.ModelSerializer):
        """Сериализатор сотрудника с отслеживанием выполненных задач"""

        active_task_count = serializers.SerializerMethodField()
        tasks = TaskSerializer(many=True)

        @staticmethod
        def get_active_task_count(obj):
            return obj.tasks.filter(is_active=True).count()

        class Meta:
            model = Employee
            fields = ('full_name', 'position', 'active_task_count', 'tasks')
            validators = [
                RelatedTaskValid(field='parent_task'),
                NestingOfTaskValid(field='parent_task'),
                StatusTaskValid(field='status'),
            ]