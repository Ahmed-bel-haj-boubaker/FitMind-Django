
from django import forms
from .models import Workout, Exercise

class WorkoutRecommendationForm(forms.Form):
    workout_type = forms.ChoiceField(
        choices=[
            ('Cardio', 'Cardio'),
            ('Strength', 'Strength'),
            ('Yoga', 'Yoga'),
            ('Pilates', 'Pilates'),
        ],
        label="Workout Type"
    )
    level = forms.ChoiceField(
        choices=Workout.WORKOUT_LEVELS,
        label="Level"
    )
class WorkoutForm(forms.ModelForm):
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=True
    )

    class Meta:
        model = Workout
        fields = ['name', 'description', 'exercises','image','level']
        
  
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'category', 'duration', 'repetitions', 'calories_burned','image']
        
