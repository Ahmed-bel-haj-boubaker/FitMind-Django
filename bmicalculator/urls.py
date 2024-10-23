from django.urls import path
from bmicalculator import views

urlpatterns = [
    path("", views.Bmi, name="bmi-calculator"),
    path("get_advice/", views.get_advice, name="get_advice"),
]
