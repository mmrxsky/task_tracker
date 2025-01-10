from django.contrib.auth.models import Group
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
            full_name="Test new", position="Test", user=self.user
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


class EmployeeModeratorTestCase(APITestCase):
    """Тесты для модели сотрудника с пользователем модератор"""

    def setUp(self):
        self.user = User.objects.create(email="moderator@test.ru", is_staff=True)
        self.my_group = Group.objects.create(name="moderator")
        self.user.groups.add(self.my_group)
        self.user2 = User.objects.create(email="test@test.ru")
        self.user3 = User.objects.create(email="test1@test.ru")
        self.employee = Employee.objects.create(
            full_name="Test 5", position="Moderator", user=self.user
        )
        self.employee2 = Employee.objects.create(
            full_name="Test 4", position="Test5", user=self.user2
        )
        self.task = Task.objects.create(
            title="Test",
            description="test",
            executor=None,
            status="ToDo",
            is_active="False",
            is_related="False",
        )
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user2)
        self.client.force_authenticate(user=self.user3)

    def test_employee_retrieve(self):
        """Тестирование вывода одного сотрудника модератором"""
        url = reverse("tracker:employees-detail", args=(self.employee2.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["full_name"], self.employee2.full_name)
        self.assertEqual(data["position"], self.employee2.position)

    def test_employee_create(self):
        """Тестирование создания сотрудника модератором"""
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:employees-list")
        data = {
            "full_name": "Test full_name 3",
            "position": "Test position 3",
            "user": self.user3,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.all().count(), 3)

    def test_employee_update(self):
        """Тестирование изменения сотрудника модератором"""
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:employees-detail", args=(self.employee2.pk,))
        data = {"full_name": "Test full_name NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("full_name"), "Test full_name NEW")

    def test_employee_delete(self):
        """Тестирование удаления пользователя модератором"""
        self.client.force_authenticate(user=self.user)
        url = reverse("tracker:employees-detail", args=(self.employee2.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.all().count(), 1)

    def test_employee_list(self):
        """Тестирование вывода списка сотрудников модератором"""
        url = reverse("tracker:employees-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "full_name": self.employee.full_name,
                "position": self.employee.position,
            },
            {
                "full_name": self.employee2.full_name,
                "position": self.employee2.position,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class TaskTestCase(APITestCase):
    """Тестирование модели задачи"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.employee = Employee.objects.create(
            full_name="Test", position="Test", user=self.user
        )
        self.task = Task.objects.create(
            id=1,
            title="test",
            description="test",
            status="In Progress",
            time_complete="2025-01-10T12:00:00Z",
            is_active=False,
            is_related=False,
            executor=None,
            parent_task=None,
        )
        self.client.force_authenticate(user=self.user)

    def test_task_retrieve(self):
        """Тестирование вывода одной задачи"""
        url = reverse("tracker:task_retrieve", args=(self.task.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.task.title)
        self.assertEqual(data["description"], self.task.description)

    def test_task_list(self):
        """Тестирование вывода списка задач"""
        url = reverse("tracker:task_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.task.pk,
                "title": self.task.title,
                "description": self.task.description,
                "status": self.task.status,
                "time_complete": self.task.time_complete,
                "is_active": False,
                "is_related": False,
                "executor": None,
                "parent_task": self.task.parent_task,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_task_create(self):
        """Тестирование создания задачи"""
        url = reverse("tracker:task_create")
        data = {
            "title": "Test3",
            "description": "test3",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": False,
            "is_related": True,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.all().count(), 1)

    def test_task_update(self):
        """Тестирование изменения задачи"""
        url = reverse("tracker:task_update", args=(self.task.pk,))
        data = {"title": "Test title NEW"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data.get("title"), None)

    def test_task_delete(self):
        """Тестирование удаления задачи модератором"""
        url = reverse("tracker:task_delete", args=(self.task.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.all().count(), 1)


class TaskModeratorTestCase(APITestCase):
    """Тесты для модели задачи модератора"""

    def setUp(self):
        self.user = User.objects.create(email="moderator@test.ru", is_staff=True)
        self.my_group = Group.objects.create(name="moderator")
        self.user.groups.add(self.my_group)
        self.employee = Employee.objects.create(
            full_name="Test", position="Moderator", user=self.user
        )
        self.task = Task.objects.create(
            id=1,
            title="test",
            description="test",
            status="In Progress",
            time_complete="2025-01-10T12:00:00Z",
            is_active=False,
            is_related=False,
            executor=None,
            parent_task=None,
        )
        self.client.force_authenticate(user=self.user)

    def test_task_create(self):
        """Тестирование создания задачи модератором"""
        url = reverse("tracker:task_create")
        data = {
            "title": "Test 3",
            "description": "test3",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": False,
            "is_related": True,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.all().count(), 2)


    def test_task_delete(self):
        """Тестирование удаления задачи модератором"""
        url = reverse("tracker:task_delete", args=(self.task.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.all().count(), 0)

    def test_related_task_validator(self):
        """Тестирование валидации связанности задачи"""
        url = reverse("tracker:task_create")
        data = {
            "title": "Test 3",
            "description": "test3",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": False,
            "is_related": False,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            ["Задача должна быть связана с родительской"],
        )

    def test_status_task_validator(self):
        """Тестирование валидации статуса задачи"""
        url = reverse("tracker:task_create")
        data = {
            "title": "Test 3",
            "description": "test3",
            "status": "ToDo",
            "parent_task": 1,
            "is_active": True,
            "is_related": True,
        }
        response = self.client.post(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors"),
            ["Активная задача должна иметь статус In Progress"],
        )
