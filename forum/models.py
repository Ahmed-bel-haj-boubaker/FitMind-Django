from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Import du modèle User par défaut

class Sujet(models.Model):
    STATUT_CHOICES = [
        ('non_resolu', 'Non Résolu'),
        ('resolu', 'Résolu'),
    ]

    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    date_update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='non_resolu')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Nullable

    def __str__(self):
        return self.titre
    
class Reaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True, blank=True)
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE , null=True, blank=True)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'sujet')  # Un utilisateur ne peut réagir qu'une fois par sujet

    def __str__(self):
        return f"{self.user.username} - {self.reaction} - {self.sujet.titre}"
    
class ReplaySujet(models.Model):
    id = models.AutoField(primary_key=True)  # ID unique
    message = models.TextField()  # Contenu du message
    date_creation = models.DateTimeField(auto_now_add=True)  # Date de création
    date_update = models.DateTimeField(auto_now=True)
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='replays')  # Référence au sujet
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Nullable

    def __str__(self):
        return f"Replay by {self.user.username} on {self.sujet.titre}"