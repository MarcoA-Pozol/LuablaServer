from django.contrib import admin
from django.urls import path, include
# Modules to manage the images routing using static path and files
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Welcome.urls')),
    path('authentication/', include('Authentication.urls')),
    path('community/', include('Community.urls')),
    path('profile/', include('Profile.urls')),
    #Languages
    path('CN/', include('Languages.Chinese.urls')),
    path('EN/', include('Languages.English.urls')),
    # API (Internal Luabla API)
    path('API/', include('Luabla_API.urls')),
]

# This is to enable Django project to serve media files during development stage.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)