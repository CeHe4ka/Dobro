from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .models import ViewLog
from django.db.models import Q
from .models import Favorite
from .models import Rating
from django.http import JsonResponse, HttpResponseBadRequest
from .models import WatchLater
from django.utils import timezone
from .forms import VideoForm

@login_required
def video_catalog(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    videos = Video.objects.all()

    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__icontains=query)
        )
    if category:
        videos = videos.filter(category__icontains=category)
    if tag:
        videos = videos.filter(tags__icontains=tag)

    # Рейтинги и избранное
    ratings = Rating.objects.filter(user=request.user)
    ratings_dict = {r.video_id: r.value for r in ratings}

    favorites = set(Favorite.objects.filter(user=request.user).values_list('video_id', flat=True))

    return render(request, 'videos/catalog.html', {
        'videos': videos,
        'query': query,
        'category': category,
        'tag': tag,
        'ratings': ratings_dict,
        'favorites': favorites,
    })

@login_required
def view_history(request):
    history = ViewLog.objects.filter(user=request.user).order_by('-viewed_at')

    return render(request, 'videos/history.html', {
        'history': history
    })


@login_required
def open_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    ViewLog.objects.update_or_create(
        user=request.user,
        video=video,
        defaults={'viewed_at': timezone.now()},
    )
    return redirect(video.youtube_url)




@login_required
def favorites(request):
    favorite_videos = Video.objects.filter(favorite__user=request.user)
    return render(request, 'videos/favorites.html', {'videos': favorite_videos})


@login_required
def rate_video(request, video_id, value):
    video = get_object_or_404(Video, pk=video_id)
    if value not in ['like', 'dislike']:
        from django.http import JsonResponse

        return JsonResponse({'status': 'ok'})

    rating, created = Rating.objects.get_or_create(user=request.user, video=video)
    rating.value = value
    rating.save()
    from django.http import JsonResponse

    return JsonResponse({'status': 'ok'})


@login_required
def remove_rating(request, video_id):
    Rating.objects.filter(user=request.user, video_id=video_id).delete()
    return redirect('accounts:profile')


@login_required
def later(request):
    user = request.user
    watch_later_entries = WatchLater.objects.filter(user=user).select_related('video')

    video_data = []
    for entry in watch_later_entries:
        video = entry.video
        is_favorite = Favorite.objects.filter(user=user, video=video).exists()
        has_liked = Rating.objects.filter(user=user, video=video, value='like').exists()
        video_data.append({
            'video': video,
            'is_favorite': is_favorite,
            'has_liked': has_liked,
        })

    return render(request, "videos/later.html", {"video_data": video_data})

@login_required
def youtube_id(value):
    """Извлекает ID из полной ссылки на YouTube"""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", value)
    return match.group(1) if match else value

def catalog_view(request):
    return render(request, 'catalog.html')

@login_required
def watch_later_view(request):
    videos = request.user.watch_later.all()

    video_data = []
    for video in videos:
        is_favorite = video in request.user.favorite_videos.all()
        has_liked = video.rating_set.filter(user=request.user, value='like').exists()
        video_data.append({
            'video': video,
            'is_favorite': is_favorite,
            'has_liked': has_liked,
        })

    return render(request, 'videos/later.html', {
        'video_data': video_data,
    })


@login_required
def toggle_watch_later(request):
    if request.method == "POST":
        try:
            video_id = request.POST.get("video_id")
            video = get_object_or_404(Video, id=video_id)

            watch_later_obj = WatchLater.objects.filter(user=request.user, video=video).first()
            if watch_later_obj:
                watch_later_obj.delete()
                return JsonResponse({"status": "ok", "watch_later": False})
            else:
                WatchLater.objects.create(user=request.user, video=video, added_at=timezone.now())
                return JsonResponse({"status": "ok", "watch_later": True})
        except Exception as e:
            # Возвращаем ошибку в JSON, чтобы увидеть в браузере
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def watch_later_list(request):
    videos = [wl.video for wl in WatchLater.objects.filter(user=request.user).select_related('video')]
    return render(request, 'videos/later.html', {'videos': videos})


def is_watch_later(request, video_id):
    if not request.user.is_authenticated:
        return JsonResponse({'watch_later': False})
    try:
        video = Video.objects.get(id=video_id)
        exists = WatchLater.objects.filter(user=request.user, video=video).exists()
        return JsonResponse({'watch_later': exists})
    except Video.DoesNotExist:
        return JsonResponse({'watch_later': False})

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Сохраняем факт просмотра
    ViewLog.objects.update_or_create(
        user=request.user,
        video=video,
        defaults={'viewed_at': timezone.now()},
    )


    return render(request, 'videos/watch_video.html', {'video': video})


@login_required
def history_view(request):
    history = ViewLog.objects.filter(user=request.user).select_related('video').order_by('-viewed_at')
    return render(request, 'videos/history.html', {'history': history})


@login_required
def toggle_favorite(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, video=video)
        if not created:
            favorite.delete()
            return JsonResponse({'status': 'ok', 'is_favorite': False})
        return JsonResponse({'status': 'ok', 'is_favorite': True})
    return HttpResponseBadRequest("Invalid method")

@login_required
def is_favorite(request, video_id):
    user = request.user
    try:
        video = Video.objects.get(id=video_id)
        is_favorite = Favorite.objects.filter(user=user, video=video).exists()
        return JsonResponse({'is_favorite': is_favorite})
    except Video.DoesNotExist:
        return JsonResponse({'is_favorite': False})

@login_required
def add_video(request):
    if not request.user.is_editor:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.author = request.user.get_full_name()  # сохраняем ФИО автора
            video.save()
            messages.success(request, "Видео добавлено.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Ошибка в форме. Проверьте поля.")
    else:
        form = VideoForm()

    return render(request, 'accounts/add_video_modal.html', {'form': form})


    return render(request, 'videos/add_video.html', {'form': form})