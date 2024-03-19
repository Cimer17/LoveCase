from .views import *
from django.urls import path, include

urlpatterns = [
    path('profile/', profiles, name='profiles'), 
    path('profile/<int:user_id>/', profile_view, name='profile'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', RegisterView.as_view(), name="register"),
    path('send_message_to_telegram/', send_message_to_telegram, name='send_message_to_telegram'),
]