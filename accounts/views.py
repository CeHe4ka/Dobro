from django.contrib.auth import login, update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, EmailAuthenticationForm
from videos.models import Rating
from videos.models import Video  # Импорт модели видео

@login_required
def dashboard(request):
    videos = Video.objects.all()  # Или фильтрованные по пользователю
    return render(request, 'accounts/dashboard.html', {'videos': videos})
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

def login_register_view(request):
    active_form = 'login'
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'register':
            registration_form = RegistrationForm(request.POST)
            form = EmailAuthenticationForm()  # пустая форма входа

            if registration_form.is_valid():
                user = registration_form.save(commit=False)
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                # если форма невалидна — остаёмся на странице и показываем ошибки
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'register_form': registration_form
                })

        elif form_type == 'login':
            form = EmailAuthenticationForm(request, data=request.POST)
            registration_form = RegistrationForm()  # пустая форма регистрации

            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                # если ошибка входа — остаёмся и показываем ошибки
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'register_form': registration_form
                })

    # GET-запрос
    form = EmailAuthenticationForm()
    registration_form = RegistrationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'register_form': registration_form,
        'active_form': active_form,
    })