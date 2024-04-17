from django.urls import path
from team_task_manager.views import (
    index
)


urlpatterns = [
    path("", index, name="index")
]


app_name = "manager"
