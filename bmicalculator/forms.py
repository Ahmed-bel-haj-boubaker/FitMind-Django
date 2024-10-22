from django import forms
from .models import BMICalculator


class BMICalculatorForm(forms.ModelForm):
    class Meta:
        model = BMICalculator
        fields = ["age", "gender", "weight", "height"]
