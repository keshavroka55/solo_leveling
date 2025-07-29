# tracker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list_view, name='task_list'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update_view, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete_view, name='task_delete'),
    path('submit-progress/', views.submit_progress_view, name='submit-progress'),
    path('daily-summary/', views.daily_summary_view, name='daily-summary'),
    path('progress-graph/', views.progress_graph_view, name='progress-graph'),
    path('update-streak-rank/', views.update_streak_and_rank, name='update-streak-rank'),
    path('notifications/', views.notifications_view, name='notifications'),
]
