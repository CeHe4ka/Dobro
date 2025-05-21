from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from videos.models import Rating



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # обязательно!
            user.is_active = True       # ← теперь активируем сразу
            user.save()
            login(request, user)
            return redirect('accounts:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})
@login_required
def profile(request):
    user = request.user
    ratings = Rating.objects.filter(user=user).select_related('video')

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user, request.POST)

        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Профиль обновлен')
            return redirect('accounts:profile')
    else:
        form = RegistrationForm(instance=user)
        password_form = PasswordChangeForm(user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'password_form': password_form,
        'ratings': ratings
    })