from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Task, TaskType, Position, Worker


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "position",
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Position", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Position", {"fields": ("first_name", "last_name", "position",)}),
    )
