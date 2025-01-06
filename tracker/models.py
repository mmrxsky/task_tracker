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
