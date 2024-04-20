from datetime import date
from django.test import TestCase
from team_task_manager.forms import TagSearchForm, WorkerForm, TaskForm, WorkerSearchForm
from team_task_manager.models import Position, Tag, TaskType, Worker


class FormTests(TestCase):
    def test_worker_creation_form_with_position_first_last_name_is_valid(self) -> None:
        position = Position.objects.create(name="develop")
        form_data = {
            "username": "new_user",
            "first_name": "Test",
            "last_name": "Last",
            "password1": "worker123",
            "password2": "worker123",
            "position": position,
        }
        form = WorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_serch_form_with_valid_data(self):
        form = WorkerSearchForm(data={"username": "Test"})
        self.assertTrue(form.is_valid())

    def test_worker_serch_form_with_invalid_data(self):
        form = WorkerSearchForm()
        self.assertFalse(form.is_valid())

    def test_tag_serch_form_with_invalid_data(self):
        form = TagSearchForm(data={"tag": "@python-refactoring"})
        self.assertTrue(form.is_valid())

    def test_tag_serch_form_with_invalid_data(self):
        form = TagSearchForm()
        self.assertFalse(form.is_valid())
