from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from team_task_manager.models import Task, TaskType, Worker


HOME_PAGE = reverse("manager:index")
WORKERS_LIST = reverse("manager:workers-list")
TASKS_LIST = reverse("manager:tasks-list")
POSITIONS_LIST = reverse("manager:positions-list")


class TestsForPublicRequired(TestCase):

    def test_login(self) -> None:
        response = self.client.get(HOME_PAGE)
        self.assertNotEqual(response.status_code, 200)

    def test_workers_list(self) -> None:
        response = self.client.get(WORKERS_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_tasks_list(self):
        response = self.client.get(TASKS_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_positions_list(self):
        response = self.client.get(POSITIONS_LIST)
        self.assertNotEqual(response.status_code, 200)


class TestsForPrivateRequired(TestCase):

    def setUp(self) -> None:
        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            password="Test123"
        )
        self.client.force_login(self.worker)

    def test_login(self) -> None:
        response = self.client.get(HOME_PAGE)
        self.assertEqual(response.status_code, 200)

    def test_workers_list(self) -> None:
        response = self.client.get(WORKERS_LIST)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["workers_list"]),
            list(Worker.objects.all())
        )

    def test_tasks_list(self):
        response = self.client.get(TASKS_LIST)
        task_type = TaskType.objects.create(name="refactoring")
        Task.objects.create(
            name="TestTask",
            priority="urgent",
            deadline=date.today(),
            is_completed=False,
            task_type=task_type
        )
        Task.objects.create(
            name="Test_Task",
            priority="low",
            deadline=date.today(),
            is_completed=True,
            task_type=task_type
        )
        tasks = Task.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["tasks_list"]),
            list(tasks)
        )

    def test_positions_list(self):
        response = self.client.get(POSITIONS_LIST)
        self.assertEqual(response.status_code, 200)
