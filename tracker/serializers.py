from django.db.models import Q, Count
from rest_framework import serializers
from tracker.models import Employee, Task
from tracker.validators import RelatedTaskValid, NestingOfTaskValid, StatusTaskValid


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор сотрудника"""

    class Meta:
        model = Employee
        fields = (
            "full_name",
            "position",
        )


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор задачи"""

    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            RelatedTaskValid(field="parent_task"),
            NestingOfTaskValid(field="parent_task"),
            StatusTaskValid(field="status"),
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
        fields = ("full_name", "position", "active_task_count", "tasks")
        validators = [
            RelatedTaskValid(field="parent_task"),
            NestingOfTaskValid(field="parent_task"),
            StatusTaskValid(field="status"),
        ]


class ImportantTaskSerializer(serializers.ModelSerializer):
    """Сериализатор выбора свободных сотрудников для важных задач"""

    tasks = TaskSerializer
    employees = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ("id", "title", "time_complete", "employees")
        validators = [
            RelatedTaskValid(field="parent_task"),
            NestingOfTaskValid(field="parent_task"),
            StatusTaskValid(field="status"),
        ]

    @staticmethod
    def get_employees(self):
        important_tasks = Task.objects.filter(
            Q(is_active=False)
            & (
                Q(parent_task__is_active=True)
                | Q(parent_task__parent_task__is_active=True)
                | Q(parent_task__parent_task__parent_task__is_active=True)
            )
        )
        imp_task_id = []
        for task in important_tasks:
            imp_task_id.append(task.id)

        employee_min_task = (
            Employee.objects.all()
            .annotate(task_count=Count("tasks"))
            .order_by("task_count")
            .first()
        )
        emt_id = employee_min_task.id
        count_employee_min_task = Task.objects.filter(executor__id=emt_id).count()
        available_employees = []
        for i in imp_task_id:
            task_parent = Task.objects.get(pk=i).parent_task
            employee_task_parent = Employee.objects.filter(
                tasks__id=task_parent.id
            ).first()
            if employee_task_parent is not None:
                etp_id = employee_task_parent.id
                count_employee_task_parent = Task.objects.filter(
                    executor__id=etp_id
                ).count()
                if count_employee_task_parent - count_employee_min_task <= 2:
                    emp = Employee.objects.filter(pk=etp_id)
                    for e in emp:
                        if e in emp:
                            if e.full_name not in available_employees:
                                available_employees.append(e.full_name)
            else:
                emp = Employee.objects.filter(pk=emt_id)
                for e in emp:
                    if e.full_name not in available_employees:
                        available_employees.append(e.full_name)
        return available_employees
