from django.shortcuts import render, redirect
from applications.events.models import *
from datetime import datetime, time
from django.core.paginator import Paginator
from applications.events import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import random
from django.contrib.auth.decorators import login_required
from . import post_reformatter, views_support_script

import django.apps

def retrieve_eventboard(request):
    current_page_num = request.GET.get('page', 1)
    # Sort by nearest upcoming events
    future_events = Event.objects.filter(date__gte=datetime.now())
    for event in future_events:
        #Reformat the date string
        event.date = str(event.date.month) + "/" + str(event.date.day) + "/" + str(event.date.year)

    paginator = Paginator(future_events, 24)
    try:
        future_events = paginator.page(current_page_num)
    except PageNotAnInteger:
        future_events = paginator.page(1)
    except EmptyPage:
        future_events = paginator.page(paginator.num_pages)

    page_range = future_events.paginator.page_range
    page_has_previous = future_events.has_previous()
    page_has_next = future_events.has_next()
    #https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    return render(request, "events/eventboard.html", {"events": future_events, "page_range": page_range,
                                                     "current_page_num": current_page_num,
                                                     "page_has_previous": page_has_previous, "page_has_next": page_has_next,
                                                    })


def retrieve_event_info(request, event_id="default"):
    #if request.method == "POST":
    #    print("POST:", request.POST)
    #else:
    print("id:", event_id)
    event = Event.objects.filter(event_id=event_id)
    event_exisists = True
    if len(event) == 0:
        event_exisists = False
        return render(request, "events/event_info.html", {"event": event[0], "event_tags": event[0].tags, "event_exists": event_exisists})
    return render(request, "events/event_info.html", {"event": event[0], "event_tags": event[0].tags, "event_exists": event_exisists})


@login_required
def create_event(request):
    if request.method == "POST":
        #Reformat the start_time/end_time.
        print("Request:", request.POST)
        print("Files from form:", request.FILES)
        updated_request_POST = request.POST.copy()
        start_time_datetime = datetime.strptime(str(request.POST["start_time"]), "%I:%M %p")
        end_time_datetime = datetime.strptime(str(request.POST["end_time"]), "%I:%M %p")
        updated_request_POST["start_time"] = str(start_time_datetime.time())
        updated_request_POST["end_time"] = str(end_time_datetime.time())
        event_form = forms.EventForm(updated_request_POST)
        event_image_form = forms.EventImageForm(updated_request_POST, request.FILES)
        location_form = forms.LocationForm(updated_request_POST)
        #print("request.FILES:", request.FILES, request.FILES[0], type(request.FILES[0]))
        #print("Form:", form.__dict__)
        if event_form.is_valid() and event_image_form.is_valid() and location_form.is_valid():
            event = event_form.save(commit=False)
            location = location_form.save()
            event.location = location
            image_storage_url = event_image_form.save_image_of(event)
            event.image_storage_url = image_storage_url
            user = request.user
            event.host = user
            event.save()
            return redirect("events:confirm_new_event", event_id=event.event_id)
        else:
            print()
            print(event_form.errors)
            print(event_image_form.errors)

    event_form = forms.EventForm()
    event_image_form = forms.EventImageForm()
    location_form = forms.LocationForm()
    return render(request, "events/new_event_form.html", {"event_form": event_form, "event_image_form": event_image_form,
                                                          "location_form": location_form})


def confirm_new_event(request, event_id):
    event = Event.objects.filter(event_id=event_id)
    return render(request, "events/new_event_confirmation.html", {"event": event[0]})