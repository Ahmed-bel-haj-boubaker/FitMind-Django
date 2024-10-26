from asyncio import Task
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from django.conf import settings
import google.generativeai as genai
import requests
import os
from background_task import background
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
# views.py

from django.shortcuts import render, redirect
from .models import Notification, UserNotification

def user_notifications(request):
    user_notifications = UserNotification.objects.filter(user=request.user)
    return render(request, 'user_notifications.html', {'user_notifications': user_notifications})

def toggle_notification(request, notification_id):
    user_notification = UserNotification.objects.get(user=request.user, notification_id=notification_id)
    user_notification.is_active = not user_notification.is_active
    user_notification.save()
    return redirect('user_notifications')




def user_active_notifications(request):
    if request.user.is_authenticated:
        active_notifications = UserNotification.objects.filter(user=request.user, is_active=True)
    else:
        active_notifications = []

    return render(request, 'active_notifications.html', {'active_user_notifications': active_notifications})
   

def user_active_notifications_restApi(request):
    if request.user.is_authenticated:
        active_notifications = UserNotification.objects.filter(user=request.user, is_active=True)
        notifications_data = [
            {
                'title': notification.notification.title,  # Assuming there's a related notification object with title
                #'message': notification.notification.message,  # Assuming there's a message field
            }
            for notification in active_notifications
        ]
    else:
        notifications_data = []

    return JsonResponse({'active_user_notifications': notifications_data})
    

openai.api_key = settings.OPENAI_API_KEY


@csrf_exempt  # Disable CSRF protection for this endpoint (only do this for API endpoints)
def chatgpt_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            # Check for specific input
            if user_message and user_message.strip().lower() == "give meals":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_message}],
                )
                chatgpt_response = response['choices'][0]['message']['content']

                return JsonResponse({"response": chatgpt_response})
            else:
                return JsonResponse({"error": "Invalid user message."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
    


###correct function
model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key=settings.GEMINI_API_KEY)
def ai_generate_description(request):
    if request.user.is_authenticated:
        active_notifications = UserNotification.objects.filter(user=request.user, is_active=True)
        notifications_data = [
            {
                'title': notification.notification.title,  # Assuming there's a related notification object with title
                #'message': notification.notification.message,  # Assuming there's a message field
            }
            for notification in active_notifications
        ]
    else:
        notifications_data = []

    if notifications_data:
        random_notification = random.choice(notifications_data)  # Select a random notification
        title = random_notification['title']  # Access the title correctly
        prompt = f"give me an random example of {title} each time different response in 1 line "
        response = model.generate_content(prompt)
        return JsonResponse({"notification": response.text})
    else:
        return JsonResponse({"notification": "No active notifications."}, status=404)



















































@background(schedule=60)  # Runs every 60 seconds; adjust as needed
def scheduled_ai_generate_description():
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    title = "meals"
    prompt = f"give me an example of {title} in 1 line"
    response = model.generate_content(prompt)
    return response.text

#scheduled_ai_generate_description(repeat=Task.DAILY)

def get_notification_RestApi(request):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    title = "meals"
    prompt = f"give me an example of {title} in 1 line"
    #response = model.generate_content(prompt)
    response = "it work"
    return JsonResponse({"description": response})


