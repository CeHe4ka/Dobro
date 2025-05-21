from django.urls import path
from .views import register,profile,dashboard
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
]
