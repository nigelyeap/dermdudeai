from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Include app-specific URLs
    path('diagnosis/', include('diagnosis.urls')),  # Routes all 'diagnosis/' paths to the app's urls.py
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)