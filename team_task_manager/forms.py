from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from team_task_manager.models import Tag, Worker, Task


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    # tags = forms.ModelChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.TextInput,
    #     required=False
    # )

    class Meta:
        model = Task
        fields = "__all__"


class TaskStatusUpdate(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("is_completed",)
