from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from team_task_manager.forms import (
    # TagForm,
    TagSearchForm,
    TaskForm,
    # TaskStatusUpdate,
    WorkerForm,
    WorkerSearchForm
)
from team_task_manager.models import Tag, Task, TaskType, Worker, Position


@login_required
def index(request) -> HttpResponse:
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_tags = Tag.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    print(num_visits)

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
        "num_tags": num_tags,
        "num_visits": num_visits,
    }

    return render(request, template_name="manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "manager/worker_list.html"
    context_object_name = "workers_list"
    paginate_by = 2

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.prefetch_related("tasks")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    template_name = "manager/worker_form.html"
    form_class = WorkerForm
    success_url = reverse_lazy("manager:workers-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    template_name = "manager/worker_form.html"
    form_class = WorkerForm
    success_url = reverse_lazy("manager:workers-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "manager/worker_confirm_delete.html"
    success_url = reverse_lazy("manager:workers-list")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "manager/worker_detail.html"
    context_object_name = "worker"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        worker = self.object

        completed_tasks = Task.objects.filter(
            assignees=worker,
            is_completed=True
        )
        not_completed_tasks = Task.objects.filter(
            assignees=worker,
            is_completed=False
        )

        context["completed_tasks"] = completed_tasks
        context["not_completed_tasks"] = not_completed_tasks
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "manager/tasks_list.html"
    context_object_name = "tasks_list"
    paginate_by = 2

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.all()
        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                tags__name__icontains=form.cleaned_data["tag"]
            )

        return queryset

    def get_context_data(self, **kwargs) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)
        tag = self.request.GET.get("tag", "")
        context["search_form"] = TagSearchForm(initial={"tag": tag})
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = "manager/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("manager:tasks-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "manager/task_confirm_delete.html"
    success_url = reverse_lazy("manager:tasks-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    context_object_name = "task_update"
    success_url = reverse_lazy("manager:tasks-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "manager/task_detail.html"
    context_object_name = "task"


class TaskStatusUpdateView(LoginRequiredMixin, View):
    model = Task

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        task.is_completed = not task.is_completed
        task.save()

        return HttpResponseRedirect(
            reverse("manager:task-detail", kwargs={"pk": pk})
        )


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "manager/positions_list.html"
    context_object_name = "positions_list"


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = ("name",)
    template_name = "manager/tag_form.html"
    success_url = reverse_lazy("manager:tasks-list")
