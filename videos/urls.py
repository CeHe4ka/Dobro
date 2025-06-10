from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_catalog, name='catalog'),
    path('catalog/', views.video_catalog, name='catalog'),
    path('history/', views.view_history, name='history'),
    path('favorites/', views.favorites, name='favorites'),
    path('later/', views.later, name='later'),
    path('watch/<int:video_id>/', views.open_video, name='watch'),
    path('rate/<int:video_id>/<str:value>/', views.rate_video, name='rate_video'),
    path('remove_rating/<int:video_id>/', views.remove_rating, name='remove_rating'),
    path('toggle_favorite/<int:video_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle_watch_later/', views.toggle_watch_later, name='toggle_watch_later'),
    path('is_watch_later/<int:video_id>/', views.is_watch_later, name='is_watch_later'),
    path('history/', views.history_view, name='history'),
    path('is_favorite/<int:video_id>/', views.is_favorite, name='is_favorite'),
    path('add/', views.add_video, name='add_video'),
    path('add-video/', views.add_video, name='add_video'),

]
