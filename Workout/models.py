from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    duration = models.IntegerField(null=True, blank=True)
    repetitions = models.IntegerField(null=True, blank=True)
    calories_burned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.name
    

class Workout(models.Model):
    WORKOUT_LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    level = models.CharField(max_length=20, choices=WORKOUT_LEVELS, default='Beginner') 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)  

    
    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=1)
    repetitions = models.IntegerField(default=10)
    rest_time = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} Progress"
    
