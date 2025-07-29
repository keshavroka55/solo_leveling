from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class TaskCategory(models.Model):
    CATEGORY_CHOICES = [
        ("Study", "Study"),
        ("Exercise", "Exercise"),
        ("Reading", "Reading"),
        ("Work", "Work"),
    ]

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Task Categories"


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.category.name}: {self.name}"
    

# 3. Daily Task Status Submission

class TaskProgress(models.Model):
    PROGRESS_CHOICES = [
        ('completed', 'Completed'),
        ('halfway', 'Halfway'),
        ('started', 'Started'),
        ('pending', 'Pending'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progresses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    progress = models.CharField(max_length=10, choices=PROGRESS_CHOICES)
    points = models.FloatField(default=0.0)
    consistency_bonus = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task', 'date')

    def calculate_points(self):
        mapping = {
            'completed': 2.0,
            'halfway': 1.0,
            'started': 0.5,
            'pending': 0.0,
        }
        return mapping.get(self.progress, 0.0)
    

class DailySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    total_points = models.FloatField(default=0)

    class Meta:
        unique_together = ['user', 'date']



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.FloatField(default=0)
    current_rank = models.CharField(max_length=2, default='E')
    last_progress_date = models.DateField(null=True, blank=True)
    streak_count = models.PositiveIntegerField(default=0)

    def update_rank(self):
        points = self.total_points
        if points >= 100000:
            rank = 'A'
        elif points >= 10000:
            rank = 'B'
        elif points >= 1000:
            rank = 'C'
        elif points >= 100:
            rank = 'D'
        else:
            rank = 'E'

        if rank != self.current_rank:
            self.current_rank = rank
            return True  # Rank changed
        return False

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)



