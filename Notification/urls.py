from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('user-notifications/', views.user_notifications, name='user_notifications'),
    path('toggle-notification/<int:notification_id>/', views.toggle_notification, name='toggle_notification'),
    path('active-notifications/', views.user_active_notifications, name='user_active_notifications'),
    path('chat/', views.chatgpt_view, name='chatgpt'),
    path('chat-interface/', TemplateView.as_view(template_name='chat.html'), name='chat_interface'),
    path('generate/', views.ai_generate_description , name="generate"),  
    path('get_ai_description/', views.get_notification_RestApi),
    path('active-notifications-api/', views.user_active_notifications_restApi)


]






 