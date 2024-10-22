from django.urls import path
from bmicalculator import views

urlpatterns = [
    path('', views.Bmi, name="bmi-calculator"),
   
]