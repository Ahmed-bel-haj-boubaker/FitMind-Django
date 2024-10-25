from django import forms
from .models import ReplaySujet

class ReplayForm(forms.ModelForm):
    class Meta:
        model = ReplaySujet
        fields = ['message'] 
