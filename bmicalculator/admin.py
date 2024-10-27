from django.contrib import admin

from .models import BMICalculator, NutritionPlan


admin.site.register(BMICalculator)
admin.site.register(NutritionPlan)
