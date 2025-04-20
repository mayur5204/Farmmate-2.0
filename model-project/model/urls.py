from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('crop/', include('crop_recommendation.urls')),
    path('users/', include('users.urls')),
    path('community/', include('community.urls')),
    
    # Always serve static and media files regardless of DEBUG setting
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]}),
]

# Alternative way to serve media and static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
