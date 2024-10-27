from django import forms
from .models import Sujet

class postForm(forms.ModelForm):
    class Meta:
        model = Sujet
        fields = ['titre', 'description', 'image' ,'statut'] 
