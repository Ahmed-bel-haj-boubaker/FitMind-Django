from django.contrib import admin
from django.urls import include, path
from test import views

urlpatterns = [path("test/", admin.site.urls),
               
                path('', views.testTemplate, name='home')]
