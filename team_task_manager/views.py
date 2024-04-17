from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from team_task_manager.models import (
    Task,
    TaskType,
    Worker
)


@login_required
def index(request) -> HttpResponse:
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types
    }

    return render(
        request,
        template_name="manager/index.html",
        context=context
    )
