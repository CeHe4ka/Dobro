from django.urls import path
from .views import profile, dashboard
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_register_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),


]
