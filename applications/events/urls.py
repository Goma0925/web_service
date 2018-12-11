from django.urls import path, include
from . import views

app_name = "events"

urlpatterns = [
    path("eventboard/", views.retrieve_eventboard, name="retrieve_eventboard"),
    path("eventboard/page=<int:page>", views.retrieve_eventboard, name="retrieve_eventboard",),
    path("events/<str:event_id>/", views.retrieve_event_info, name="retrieve_event_info"),
    path("create_event/", views.create_event, name="create_event"),
]
