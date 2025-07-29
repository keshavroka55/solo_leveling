from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, TaskCategory
from .forms import TaskForm

from .models import TaskProgress
from datetime import date

@login_required
def task_list_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})






from django.shortcuts import render, redirect
from .models import Task, TaskProgress, DailySummary, UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Sum


@login_required
def submit_progress_view(request):
    tasks = Task.objects.filter(user=request.user)
    today = now().date()

    if request.method == 'POST':
        for task in tasks:
            progress_value = float(request.POST.get(f'progress_{task.id}', 0))
            previous_day = today - timedelta(days=1)

            # Check if yesterday's progress exists
            yesterday_entry = TaskProgress.objects.filter(task=task, date=previous_day,user=request.user).exists()
            bonus = yesterday_entry and progress_value > 0

            progress_obj, created = TaskProgress.objects.get_or_create(
                task=task, date=today, user= request.user,
                defaults={'progress': progress_value, 'consistency_bonus': bonus}
            )

            if not created:
                progress_obj.progress = progress_value
                progress_obj.consistency_bonus = bonus
                progress_obj.save()

        return redirect('daily-summary')

    return render(request, 'submit_progress.html', {'tasks': tasks})


@login_required
def daily_summary_view(request):
    today = now().date()
    user = request.user
    tasks = Task.objects.filter(user=user)
    progress_entries = TaskProgress.objects.filter(task__in=tasks, date=today)

    total_points = 0
    for entry in progress_entries:
        total_points += round(float(entry.progress))
        if entry.consistency_bonus:
            total_points += 1

    DailySummary.objects.update_or_create(
        user=user, date=today, defaults={'total_points': total_points}
    )

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.total_points += total_points
    profile.save()

    return render(request, 'daily_summary.html', {
        'today': today,
        'progress_entries': progress_entries,
        'total_points': total_points,
        'lifetime_points': profile.total_points,
    })


# progress view graph

from .models import DailySummary, UserProfile, Notification


def progress_graph_view(request):
    user = request.user
    # Fetch last 30 days of points
    today = now().date()
    start_date = today - timedelta(days=30)

    summaries = DailySummary.objects.filter(user=user, date__gte=start_date).order_by('date')

    dates = [summary.date.strftime('%Y-%m-%d') for summary in summaries]
    points = [summary.total_points for summary in summaries]

    return render(request, 'progress_graph.html', {
        'dates': dates,
        'points': points,
    })



def update_streak_and_rank(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    today = now().date()
    yesterday = today - timedelta(days=1)

    # Check if user submitted progress today
    from .models import TaskProgress
    submitted_today = TaskProgress.objects.filter(task__user=user, date=today).exists()

    if not submitted_today:
        profile.streak_count = 0  # streak broken
        profile.save()
        return redirect('dashboard')

    # Check if yesterday progress exists
    submitted_yesterday = TaskProgress.objects.filter(task__user=user, date=yesterday).exists()

    if submitted_yesterday:
        profile.streak_count += 1
    else:
        profile.streak_count = 1  # restart streak

    # Update last progress date
    profile.last_progress_date = today

    # Update total points (sum all progress points)
    daily_summary = DailySummary.objects.filter(user=user, date=today).first()
    if daily_summary:
        profile.total_points += daily_summary.total_points

    # Check and update rank
    rank_changed = profile.update_rank()

    profile.save()

    # Send notifications
    if rank_changed:
        Notification.objects.create(
            user=user,
            message=f"🎉 Congrats! Your rank has been upgraded to {profile.current_rank}!"
        )

    # Notify streak milestones
    milestones = [7, 21, 60, 90]
    if profile.streak_count in milestones:
        Notification.objects.create(
            user=user,
            message=f"🔥 You have a {profile.streak_count}-day streak! Keep it up!"
        )

    return redirect('dashboard')


def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifs})
