# tasks_management/models.py
from django.conf import settings
from django.db import models

class Task(models.Model):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, db_index=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        on_delete=models.CASCADE
    )

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_by"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"
