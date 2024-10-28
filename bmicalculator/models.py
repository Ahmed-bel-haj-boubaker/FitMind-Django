from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def calculate_bmi(weight, height):
    height_meters = height / 100
    return round(weight / (height_meters**2), 2)


class NutritionPlan(models.Model):
    text = models.TextField(
        blank=True,
        null=True,
    )
    bmi_calculator = models.ForeignKey(
        "BMICalculator", on_delete=models.CASCADE, null=True
    )  # Set null=True here

    def __str__(self):
        return (
            f"Nutrition Plan (BMI: {self.bmi_calculator.bmi})"
            if self.bmi_calculator
            else "Nutrition Plan"
        )


class BMICalculator(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.FloatField(help_text="Weight in kilograms")
    height = models.FloatField(help_text="Height in cm")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nutrition_plan = models.ForeignKey(
        NutritionPlan, on_delete=models.SET_NULL, null=True, blank=True
    )

    bmi = models.FloatField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.height <= 0:
            raise ValidationError("Height must be greater than 0.")
        if self.weight <= 0:
            raise ValidationError("Weight must be greater than 0.")

        self.bmi = calculate_bmi(self.weight, self.height)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"BMI: {self.bmi}"
