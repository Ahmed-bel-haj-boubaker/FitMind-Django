from django import forms
from .models import Sujet

class SujetForm(forms.ModelForm):
    class Meta:
        model = Sujet
        fields = ['titre', 'description', 'image' ] 
