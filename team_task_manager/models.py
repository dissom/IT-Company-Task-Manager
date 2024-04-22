from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True
    )

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        verbose_name = "position"
        verbose_name_plural = "positions"

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self) -> str:
        return reverse("manager:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    name = models.CharField(max_length=63)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks",
        blank=False
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.get_priority_display()})"

    def get_absolute_url(self) -> str:
        return reverse("manager:task-detail", kwargs={"pk": self.pk})
