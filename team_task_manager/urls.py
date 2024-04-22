from django.urls import path
from team_task_manager.views import (
    index,
    TagCreateView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    TaskDeleteView,
    TaskUpdateView,
    TaskStatusUpdateView,
    WorkerListView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDetailView,
    WorkerDeleteView,
    PositionListView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="workers-list"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="tasks-list"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "task/<int:pk>/update-status/",
        TaskStatusUpdateView.as_view(),
        name="task-status-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "task/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="positions-list"
    ),
    path(
        "tag/create/",
        TagCreateView.as_view(),
        name="tag-create"
    ),
]


app_name = "manager"
