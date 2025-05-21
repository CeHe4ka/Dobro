from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('catalog/', views.video_catalog, name='catalog'),
    path('history/', views.view_history, name='history'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.view_history, name='history'),
    path('watch/<int:video_id>/', views.open_video, name='watch'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/<int:video_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('rate/<int:video_id>/<str:value>/', views.rate_video, name='rate_video'),
    path('remove_rating/<int:video_id>/', views.remove_rating, name='remove_rating'),
    path('toggle_favorite/<int:video_id>/', views.toggle_favorite, name='toggle_favorite'),


]
