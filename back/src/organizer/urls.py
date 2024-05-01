from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .spectacular import urlpatterns as spectacular_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('api.urls')),
]

urlpatterns += spectacular_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
