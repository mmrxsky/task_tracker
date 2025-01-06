from rest_framework.serializers import ValidationError


class RelatedTaskValid:
    """Проверка связанной задачи на то что имеет родительскую"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        parent_task = value.get(self.field)
        is_related = value.get("is_related")
        if (parent_task is not None and not is_related) or (
            parent_task is None and is_related
        ):
            raise ValidationError("Задача должна быть связана с родительской")


class StatusTaskValid:
    """Проверка статуса активной задачи"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        status = value.get(self.field)
        is_active = value.get("is_active")
        if (status == "ToDo" or status == "Done" or status == "Closed") and is_active:
            raise ValidationError("Активная задача должна иметь статус In Progress")
        if status == "In Progress" and not is_active:
            raise ValidationError("Активная задача должна иметь статус In Progress")


class NestingOfTaskValid:
    """Проверка вложенности задачи"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        parent_task = value.get(self.field)
        if parent_task.parent_task is not None:
            if parent_task.parent_task.parent_task is not None:
                raise ValidationError("Вложенность задач не более 3")
