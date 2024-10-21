from django.urls import path
from AuthApp import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('signup',views.signup,name="signup"),
    path('login',views.handlelogin, name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),
]