from django import forms
from .models import Category, Event

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl placeholder-gray-400"


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "category",
            "nom",
            "description",
            "espace",
            "age_range",
            "date",
            "place",
            "image",
        )
        widgets = {
            "category": forms.Select(
                attrs={
                    "placeholder": "Enter your category",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "nom": forms.TextInput(
                attrs={
                    "placeholder": "Enter event's name",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter event's description",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "espace": forms.Select(
                attrs={
                    "placeholder": "select space's type",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "age_range": forms.Select(
                attrs={
                    "placeholder": "select an age range",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "place": forms.TextInput(
                attrs={
                    "placeholder": "add event place",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c; color:#f8fafc",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c; color:#f8fafc",
                }
            ),
        }


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "category",
            "nom",
            "description",
            "espace",
            "age_range",
            "date",
            "place",
            "image",
        )
        widgets = {
            "category": forms.Select(
                attrs={
                    "placeholder": "Enter your category",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "nom": forms.TextInput(
                attrs={
                    "placeholder": "Enter event's name",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter event's description",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "espace": forms.Select(
                attrs={
                    "placeholder": "select space's type",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "age_range": forms.Select(
                attrs={
                    "placeholder": "select an age range",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c;; color:#f8fafc",
                }
            ),
            "place": forms.TextInput(
                attrs={
                    "placeholder": "add event place",
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c; color:#f8fafc",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "w-full py-4 px-6 rounded-xl",
                    "style": "background-color: #44403c; color:#f8fafc",
                }
            ),
        }
