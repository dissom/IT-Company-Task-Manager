from django.db import models
from django.contrib.auth.models import AbstractUser


class TaskType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


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
