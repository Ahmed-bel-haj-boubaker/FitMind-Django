"""
URL configuration for fitmind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls), 
    #path("", include("test.urls")),
    path("", include('AuthApp.urls')),
    path('forum/', include('forum.urls')),
    path('notifications/',include('Notification.urls')),
    path("admin/", admin.site.urls),
    path("", include("AuthApp.urls")),
    path("forum/", include("forum.urls")),
    path("", include("Workout.urls")),
    path("", include('recognition.urls')),
    path("bmi-calculator/", include("bmicalculator.urls")),
    

    ]
  

if settings.DEBUG:  # Assure que cela ne fonctionne qu'en mode DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
