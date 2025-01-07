from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tracker.models import Employee, Task
from users.models import User


class EmployeeTestCase(APITestCase):
    """Тестирование модели сотрудника"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.employee = Employee.objects.create(
            full_name="Test Testov", position="Test", user=self.user
        )
        self.task = Task.objects.create(
            title="Test",
            description="test",
            executor=self.employee,
            status="ToDo",
            is_active="False",
            is_related="False",
        )
        self.client.force_authenticate(user=self.user)

    def test_employee_retrieve(self):
        """Тестирование вывода одного сотрудника"""
        url = reverse("tracker:employees-detail", args=(self.employee.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["full_name"], self.employee.full_name)
        self.assertEqual(data["position"], self.employee.position)

    def test_employee_create(self):
        """Тестирование создания сотрудника"""
        url = reverse("tracker:employees-list")
        data = {
            "full_name": "Test full_name 2",
            "position": "Test position 2",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employee_update(self):
        """Тестирование изменения пользователя"""
        url = reverse("tracker:employees-detail", args=(self.employee.pk,))
        data = {"full_name": "Test full_name NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("full_name"), "Test full_name NEW")

    def test_employee_delete(self):
        """Тестирование удаления пользователя"""
        url = reverse("tracker:employees-detail", args=(self.employee.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employee_list(self):
        """Тестирование вывода списка сотрудников"""
        url = reverse("tracker:employees-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "full_name": self.employee.full_name,
                "position": self.employee.position,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
