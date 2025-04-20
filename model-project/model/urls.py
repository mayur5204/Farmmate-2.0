from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

# Custom view to serve media files in production
def serve_media_in_production(request, path):
    """Custom view to serve media files in production environments"""
    media_root = settings.MEDIA_ROOT
    return serve(request, path, document_root=media_root)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('crop/', include('crop_recommendation.urls')),
    path('users/', include('users.urls')),
    path('community/', include('community.urls')),
    
    # Always serve media files regardless of DEBUG setting
    path('media/<path:path>', serve_media_in_production),
    
    # Serve static files directly
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT or settings.STATICFILES_DIRS[0]}),
]

# Add static/media URLs as a fallback
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
