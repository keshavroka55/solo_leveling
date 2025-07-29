from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # redirect after login
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})




