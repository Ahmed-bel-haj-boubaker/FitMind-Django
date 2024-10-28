from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, related_name="categories", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Event(models.Model):
    category = models.ForeignKey(
        Category, related_name="events", on_delete=models.CASCADE
    )

    AGE_RANGE_CHOICES = [
        ("enfants", "Enfants (-12)"),
        ("adolescents", "Adolescents (12-18)"),
        ("jeunes_adultes", "Jeunes adultes(-18-30)"),
        ("adultes", "Adultes(30-50)"),
        ("seniors", "Seniors(50+)"),
        ("non_specifie", "Non spécifié"),
    ]

    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    description = models.TextField()
    espace = models.CharField(
        max_length=50, choices=[("fermé", "Espace fermé"), ("plein_air", "Plein air")]
    )
    age_range = models.CharField(max_length=20, choices=AGE_RANGE_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    place = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, related_name="events", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="event_images", blank=True, null=True)

    # Fields to store AI-generated data
    suggested_tags = models.CharField(max_length=255, null=True)  # Requires Django 3.1+
    quote = models.CharField(max_length=255, null=True)
    difficulty_score = models.IntegerField(default=0)
    visibility_score = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
