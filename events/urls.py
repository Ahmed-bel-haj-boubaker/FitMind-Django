from django.urls import path
from .views import ma_vue, show, add_event, event_detail, delete_event, edit_event


urlpatterns = [
    path("", show, name="event_list"),
    path("add/", add_event, name="addEvent"),
    path("event/<int:event_id>/", event_detail, name="event_detail"),
    path("<int:event_id>/delete", delete_event, name="delete"),
    path("event/<int:event_id>/edit", edit_event, name="edit"),
]
