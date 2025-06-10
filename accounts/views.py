from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, EmailAuthenticationForm, ProfileUpdateForm
from videos.models import Rating, Video
from videos.forms import VideoForm

def login_register_view(request):
    active_form = 'login'
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'register':
            registration_form = RegistrationForm(request.POST)
            form = EmailAuthenticationForm()

            if registration_form.is_valid():
                user = registration_form.save(commit=False)
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('accounts:dashboard')
            return render(request, 'accounts/login.html', {
                'form': form,
                'register_form': registration_form
            })

        elif form_type == 'login':
            form = EmailAuthenticationForm(request, data=request.POST)
            registration_form = RegistrationForm()

            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('accounts:dashboard')
            return render(request, 'accounts/login.html', {
                'form': form,
                'register_form': registration_form
            })

    form = EmailAuthenticationForm()
    registration_form = RegistrationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'register_form': registration_form,
        'active_form': active_form,
    })

@login_required
def dashboard(request):
    videos = Video.objects.filter(is_approved=True)
    return render(request, 'accounts/dashboard.html', {'videos': videos})

@login_required
def request_editor_status(request):
    if request.method == 'POST' and not request.user.is_editor and not request.user.is_editor_request:
        request.user.is_editor_request = True
        request.user.save()
        messages.success(request, "Заявка отправлена.")
    return redirect('accounts:profile')

@login_required
def profile(request):
    user = request.user
    ratings = Rating.objects.filter(user=user).select_related('video')
    video_form = VideoForm()

    if request.method == 'POST':
        # Обновление профиля
        if 'change_profile' in request.POST:
            form = ProfileUpdateForm(request.POST, instance=user)
            password_form = PasswordChangeForm(user=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль обновлен.')
                return redirect('accounts:profile')

        # Смена пароля
        elif 'change_password' in request.POST:
            form = ProfileUpdateForm(instance=user)
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль обновлен.')
                return redirect('accounts:profile')

        # Смена аватара
        elif 'change_avatar' in request.POST:
            form = ProfileUpdateForm(instance=user)
            password_form = PasswordChangeForm(user=user)
            avatar = request.FILES.get('avatar')
            if avatar:
                user.avatar = avatar
                user.save()
                messages.success(request, 'Аватар обновлен.')
            return redirect('accounts:profile')

        # Отправка заявки на редактора
        elif 'editor_request' in request.POST:
            form = ProfileUpdateForm(instance=user)
            password_form = PasswordChangeForm(user=user)
            social_link = request.POST.get('social_link')

            if social_link:
                user.editor_social_link = social_link
                user.is_editor_request = True
                user.save()
                messages.success(request, 'Заявка на статус редактора отправлена.')
            else:
                messages.error(request, 'Пожалуйста, укажите ссылку на вашу соцсеть.')
            return redirect('accounts:profile')


        # Добавление видео редактором
        elif 'add_video' in request.POST and user.is_editor:
            video_form = VideoForm(request.POST, request.FILES)
            form = ProfileUpdateForm(instance=user)
            password_form = PasswordChangeForm(user=user)
            if video_form.is_valid():
                video = video_form.save(commit=False)
                video.author = user
                video.is_approved = False
                video.save()
                messages.success(request, 'Видео успешно добавлено.')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Ошибка при добавлении видео. Проверьте форму.')

    else:
        form = ProfileUpdateForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'password_form': password_form,
        'ratings': ratings,
        'video_form': video_form,
    })


def is_editor(user):
    return user.is_authenticated and user.is_editor

@login_required
def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user.get_full_name() or request.user.email
            video.save()
            messages.success(request, "Видео успешно добавлено.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Форма содержит ошибки. Проверьте поля.")
    else:
        form = VideoForm()

    return render(request, 'accounts/add_video_modal.html', {'form': form})