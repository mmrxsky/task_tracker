from django.db import models

from users.models import NULLABLE


class Employee(models.Model):
    """Модель сотрудника"""

    full_name = models.CharField(max_length=200, **NULLABLE, verbose_name='ФИО', help_text='Введите Фамилию, имя и отчество')
    position = models.CharField(max_length=250, **NULLABLE, verbose_name='Должность', help_text='Укажите должность работника')

    def __str__(self):
        return f'{self.full_name} - {self.position}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Task(models.Model):
    """Модель задачи"""

    title = models.CharField(max_length=250, verbose_name='Название задачи')
    description = models.TextField(**NULLABLE, verbose_name='Описание задачи')
    executor = models.ForeignKey(Employee, on_delete=models.CASCADE, **NULLABLE, related_name='tasks', verbose_name='исполнитель задачи')
    status = models.CharField(max_length=50, **NULLABLE, verbose_name='Статус')
    time_complete = models.DateTimeField(**NULLABLE, verbose_name='Дата и время выполнения')

    def __str__(self):
        return f'{self.title}  {self.executor}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
