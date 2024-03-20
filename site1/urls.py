import site1.settings as settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from site1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('case.urls')),
    path('', include('promocode.urls')),
    path('', include('profiles.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
