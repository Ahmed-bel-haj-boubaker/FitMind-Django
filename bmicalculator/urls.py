from django.urls import path
from bmicalculator import views

urlpatterns = [
    path("", views.Bmi, name="bmi-calculator"),
    path("get_advice/", views.get_advice, name="get_advice"),
    path("list_bmi/", views.ListBmi, name="list_bmi"),
    path("bmi/<int:id>/", views.get_bmi_by_id, name="bmi_details"),
    path("bmi/update/<int:id>/", views.update_bmi, name="update_bmi"),
    path("bmi/delete/<int:id>/", views.delete_bmi, name="delete_bmi"),
    path(
        "nutrition-plan/<int:id>/",
        views.generateNutritionPlan,
        name="get_nutrition_plan",
    ),
]
