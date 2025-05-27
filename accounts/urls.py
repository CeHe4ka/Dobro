from django.urls import path
from .views import register, profile, dashboard, login_view
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile')

]
