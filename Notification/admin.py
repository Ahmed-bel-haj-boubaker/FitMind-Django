from django.contrib import admin
from .models import Notification
from django.contrib.auth.models import User
# Register your models here.
from django.contrib import admin
from .models import Notification, UserNotification

class UserNotificationInline(admin.TabularInline):
    model = UserNotification
    extra = 0

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message')
    inlines = [UserNotificationInline]
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  
            all_users = User.objects.all()
            for user in all_users:
                UserNotification.objects.create(user=user, notification=obj, is_active=True)