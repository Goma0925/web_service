from django.urls import path, include
from applications.events import views

app_name = "events"

urlpatterns = [
    path("eventboard/", views.retrieve_eventboard, name="retrieve_eventboard"),
    path("eventboard/page=<int:page>", views.retrieve_eventboard, name="retrieve_eventboard",),
    path("events/", views.retrieve_event_info, name="retrieve_event_info"),
    path("events/<str:event_id>/", views.retrieve_event_info, name="retrieve_event_info"),
    path("events/<str:event_id>/edit_event/", views.edit_event_info, name="edit_event_info"),
    path("create_event/", views.create_event, name="create_event"),
    path("create_new/confirm/<str:event_id>/", views.confirm_new_event, name="confirm_new_event"),
]
