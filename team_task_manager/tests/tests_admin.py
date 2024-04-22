from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from team_task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin123"
        )
        self.client.force_login(self.admin_user)

        position = Position.objects.create(name="develop")

        self.worker = get_user_model().objects.create_user(
            username="author", password="author123", position=position
        )

    def test_worker_position_listed(self) -> None:

        url = reverse("admin:team_task_manager_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position.name)

    def test_author_detail_pseudonym_listed(self) -> None:

        url = reverse(
            "admin:team_task_manager_worker_change",
            args=[self.worker.id]
        )
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_author_add_fieldsets_pseudonym(self) -> None:

        url = reverse("admin:team_task_manager_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "position")
