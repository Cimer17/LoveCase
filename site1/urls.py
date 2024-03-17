import site1.settings as settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from site1.views import *
from .views import RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('case.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', profile_view, name='profile'),
    path('register', RegisterView.as_view(), name="register"),
    path('gethash/', gethash, name='gethash'),
    path('send_message_to_telegram/', send_message_to_telegram, name='send_message_to_telegram')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
