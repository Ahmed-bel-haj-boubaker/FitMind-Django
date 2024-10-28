import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Event, Category
from .forms import NewEventForm, EditEventForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

API_KEY = "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"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def ma_vue(request):
    return render(request, "events/addEvent.html")


def show(request):
    events = Event.objects.all()

    # Print the image URLs for each event
    for event in events:
        if event.image:  # Check if the image field is not empty
            print("Event Name:", event.nom)
            print("Image URL:", event.image.url)
        else:
            print("Event Name:", event.nom)
            print("Image URL: No image associated")

    categories = Category.objects.all()
    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "categories": categories,
        },
    )


@login_required
def add_event(req):
    if req.method == "POST":
        form = NewEventForm(req.POST, req.FILES)
        if form.is_valid():
            # Save the initial event data
            event = form.save(commit=False)
            event.created_by = req.user
            event.save()  # Save event to get the primary key in DB

            # Prepare event data for API call
            event_data = {
                "nom": event.nom,
                "description": event.description,
                "espace": event.espace,
                "age_range": event.age_range,
                "date": event.date,
                "place": event.place,
            }

            # Get additional data from the AI model
            ai_data = process_event_data(event_data)

            # Update event with AI data and save it in the same row
            event.suggested_tags = ai_data.get("suggested_tags", "")
            event.quote = ai_data.get("quote", "")
            event.difficulty_score = ai_data.get("difficulty_score", 0)
            event.visibility_score = ai_data.get("visibility_score", 0)
            event.save()  # Save again to update with AI data in the same row

            return redirect("/events/")
    else:
        form = NewEventForm()

    return render(req, "events/addEvent.html", {"form": form, "title": "Add Event"})


def process_event_data(event_data):
    prompt = (
        f"Given the following event details:\n"
        f"Name: {event_data['nom']}\n"
        f"Description: {event_data['description']}\n"
        f"Space: {event_data['espace']}\n"
        f"Age Range: {event_data['age_range']}\n"
        f"Date: {event_data['date']}\n"
        f"Place: {event_data['place']}\n"
        f"Please provide the suggested_tags, quote, difficulty_score from 0 to 10, and visibility_score from 0 to 10."
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data)
    response_json = response.json()

    print(response_json)

    if response.status_code == 200:
        response_json = response.json()
        output_message = response_json["choices"][0]["message"]["content"]
        return eval(
            output_message
        )  # Convert string representation of dict back to a dict
    else:
        return {
            "suggested_tags": "",
            "quote": "",
            "difficulty_score": 0,
            "visibility_score": 0,
        }


@login_required
def edit_event(req, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=req.user)

    if req.method == "POST":
        form = EditEventForm(req.POST, req.FILES, instance=event)
        if form.is_valid():
            form.save()
            print("Form saved successfully.")  # Debugging output
            return redirect("/events/")  # Confirm this path matches your URL patterns
        else:
            print(
                "Form errors:", form.errors
            )  # Print form validation errors for debugging
    else:
        form = EditEventForm(
            instance=event
        )  # Initialize the form with existing event data

    return render(req, "events/addEvent.html", {"form": form, "title": "Edit Event"})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_creator = event.created_by == request.user
    return render(
        request, "events/event_detail.html", {"event": event, "is_creator": is_creator}
    )


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    event.delete()
    return redirect("/events/")


# @login_required
# def add_category(req):
#     if req.method == "POST":
#         form = NewCategoryForm(req.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.created_by = (
#                 req.user
#             )  # If `created_by` field exists in the Category model
#             category.save()
#             return redirect(
#                 "category:list"
#             )  # Adjust "category:list" to your category list view's URL name
#     else:
#         form = NewCategoryForm()

#     return render(req, "category/form.html", {"form": form, "title": "Add Category"})
