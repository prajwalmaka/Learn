from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('classes/', include('classes.urls')),
    path('assignments/', include('assignments.urls')),
    path('performance/', include('performance.urls')),
    path('', include('core.urls')),  # For dashboard/homepage
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)