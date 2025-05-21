from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .models import ViewLog
from django.db.models import Q
from .models import Favorite
from .models import Rating
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
    ViewLog.objects.create(user=request.user, video=video)
    return redirect(video.youtube_url)

@login_required
def toggle_favorite(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, video=video)

    if not created:
        favorite.delete()  # если уже в избранном — убираем
    return redirect('videos:catalog')


@login_required
def favorites(request):
    favorite_videos = Video.objects.filter(favorite__user=request.user)
    return render(request, 'videos/favorites.html', {'videos': favorite_videos})


@login_required
def rate_video(request, video_id, value):
    video = get_object_or_404(Video, pk=video_id)
    if value not in ['like', 'dislike']:
        return redirect('videos:catalog')

    rating, created = Rating.objects.get_or_create(user=request.user, video=video)
    rating.value = value
    rating.save()
    return redirect('videos:catalog')


@login_required
def remove_rating(request, video_id):
    Rating.objects.filter(user=request.user, video_id=video_id).delete()
    return redirect('accounts:profile')


