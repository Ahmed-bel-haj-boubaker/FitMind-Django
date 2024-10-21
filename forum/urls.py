from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='forum_home'),  # Notez que nous avons donné un nom à cette URL : 'forum_home'
    # Ajoutez d'autres routes si nécessaire
]