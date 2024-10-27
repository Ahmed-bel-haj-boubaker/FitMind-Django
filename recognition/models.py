from django.db import models

class WorkoutImage(models.Model):
    image = models.ImageField(upload_to='workout_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
