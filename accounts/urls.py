from django.urls import path
from .views import signup, user_activate, dashboard


urlpatterns = [
    path('signup', signup, name='signup'),
    path('dashboard', dashboard, name='dashboard'),
    path('<str:username>/activate', user_activate, name='user_activate'),
]
