from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='forum_home'), 
    path('add', views.addSujet, name='forum_add'),
    path('<int:pk>/edit/', views.editSujet, name='forum_edit'),
    path('<int:pk>/details', views.indexReplay, name='forum_replay'),
     path('<int:pk>/delete/', views.sujet_delete, name='forum_delete'),
     path('<int:pk>/deleteReplay/', views.replay_delete, name='replay_delete'),
    path('replay/<int:pk>/edit/', views.replay_edit, name='replay_edit'),


]