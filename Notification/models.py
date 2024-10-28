from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.title

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'notification')

    def __str__(self):
        return f"{self.user.username} - {self.notification.title}"
    


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.notification.title}"