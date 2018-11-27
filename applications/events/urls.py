from django.urls import path, include
from . import views

app_name = "events"

urlpatterns = [
    path("eventboard/", views.eventboard, name="eventboard"),
    path("eventboard/page=<int:page>", views.eventboard, name="eventboard",),
    path("events/<str:event_id>/", views.event_page, name="event_page"),
]
