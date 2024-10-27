from django import forms
from .models import WorkoutImage

class WorkoutImageForm(forms.ModelForm):
    class Meta:
        model = WorkoutImage
        fields = ['image']
