from django.urls import path
from .api import RegisterAPIView, LoginAPIView

app_name = 'accounts_api'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
