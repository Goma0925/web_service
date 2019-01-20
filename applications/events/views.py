#Django libs
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
#Django modules
from applications.events.models import *
from applications.events import forms
#Python modules
from datetime import datetime
import random
#Additional Django libs
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from . import post_reformatter, views_support_script
import django.apps

def retrieve_eventboard(request):
    current_page_num = request.GET.get('page', 1)
    # Sort by nearest upcoming events
    today = timezone.now()
    future_events = Event.objects.filter(start_date__gte=today)
    for event in future_events:
        print("STM:", event.start_time)
        #pass
        #Reformat the date string
        #event.start_time = str(event.date.month) + "/" + str(event.date.day) + "/" + str(event.date.year)
        #event.end_time = str(event.date.month) + "/" + str(event.date.day) + "/" + str(event.date.year)

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
    print("request", request)
    if request.method == "POST":
        print("POST CONTENT:", request.POST)
        if request.user.is_authenticated:
            print("USER LOGGED IN")
            if request.POST.get("bookmark_request") == "add-to-watch":
                user = request.user
                if not user.has_it_in_watch_list(event_id): #Join list.
                    print("Event not in watch list")
                    user.add_to_watch_list(event_id)
                else:
                    print("Event not in watch list")
                    user.remove_from_watch_list(event_id)
            elif request.POST.get("bookmark_request") == "join-event":
                user = request.user
                if not user.has_it_in_join_list(event_id): #Watch list.
                    user.add_to_join_list(event_id)
                    print("Event not in join list")
                else: #Watch list.
                    user.remove_from_join_list(event_id)
                    print("Event not in join list")
        else:
            return render(request, "users/user_login.html")
    event_query = Event.objects.filter(event_id=event_id)
    if len(event_query) == 0:
        event_exisists = False
        event = None
    else:
        event = event_query[0] #Extract event obj from queryset
        event_exisists = True

    bookmark_request_form = forms.BookmarkRequestForm()

    if request.user.is_authenticated:
        added_to_watch_list = request.user.has_it_in_watch_list(event_id)
        added_to_join_list = request.user.has_it_in_join_list(event_id)
    else:
        added_to_watch_list = False
        added_to_join_list = False

    context_dict = {"event": event, "event_tags": event.tags.all(),
                      "event_exists": event_exisists,
                      "bookmark_request_form": bookmark_request_form,
                      "added_to_watch_list": added_to_watch_list,
                      "added_to_join_list": added_to_join_list
                      }
    return render(request, "events/event_info.html", context_dict)

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
        if event_form.is_valid() and event_image_form.is_valid() and location_form.is_valid():
            event = event_form.save(commit=False)
            location = location_form.save()
            event.location = location
            image_storage_url = event_image_form.save_image_of(event)
            event.image_storage_url = image_storage_url
            user = request.user
            event.host = user
            event.save()
            event_form.save_m2m() #To save tags field.
            return redirect("events:confirm_new_event", event_id=event.event_id)
        else:
            print("FORM ERRORS:")
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
