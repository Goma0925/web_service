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
from . import views_support_scripts
import django.apps

def retrieve_eventboard(request, search_query=""):
    is_searching = False
    has_no_result = False
    search_string = ""
    current_page_num = request.GET.get('page', 1)
    # Sort by nearest upcoming events
    if request.method == "GET" and "search_string" in request.GET:
        is_searching = True
        search_string = request.GET['search_string']
        query_string = request.GET['search_string']
        entry_query = views_support_scripts.get_query(query_string, ['name'])
        events_found = Event.objects.filter(entry_query).order_by('start_date')
        if len(events_found) == 0:
            has_no_result = True
        #print("Seached:", events_found)
    else:
        today = timezone.now()
        events_found = Event.objects.filter(start_date__gte=today).order_by('start_date')

        #print("Query-type:", type(events_found))
    for event in events_found:
        #Reformat the date string
        event.start_date = str(event.start_date.month) + "/" + str(event.start_date.day)
        event.end_date = str(event.end_date.month) + "/" + str(event.end_date.day)
        #event.start_time = str(event.end_time)
        #event.end_time = str(event.end_time)
        #print(event.start_date)
        #print(event.end_date)
        #print(event.start_time)
        #print(event.end_time)

    paginator = Paginator(events_found, 24)
    try:
        events_found = paginator.page(current_page_num)
    except PageNotAnInteger:
        events_found = paginator.page(1)
    except EmptyPage:
        events_found = paginator.page(paginator.num_pages)

    page_range = events_found.paginator.page_range
    page_has_previous = events_found.has_previous()
    page_has_next = events_found.has_next()
    #https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    return render(request, "events/eventboard.html", {"events": events_found, "page_range": page_range,
                                                     "current_page_num": current_page_num,
                                                     "page_has_previous": page_has_previous, "page_has_next": page_has_next,
                                                     "search_string": search_string,
                                                     "is_searching": is_searching,
                                                     "has_no_result": has_no_result,
                                                    })


def retrieve_event_info(request, event_id="default"):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("bookmark_request") == "add-to-watch":
                user = request.user
                if not user.has_it_in_watch_list(event_id):
                    user.add_to_watch_list(event_id)
                else:
                    user.remove_from_watch_list(event_id)
            elif request.POST.get("bookmark_request") == "join-event":
                user = request.user
                if not user.has_it_in_join_list(event_id):
                    user.add_to_join_list(event_id)
                else:
                    user.remove_from_join_list(event_id)
        else:
            return render(request, "users/user_login.html")
    event_query = Event.objects.filter(event_id=event_id)
    if len(event_query) == 0:
        event_exisists = False
        event = None
    else:
        event = event_query[0] #Extract event obj from queryset
        event_exisists = True
        host_name = event.host.profile.first_name + " " + event.host.profile.last_name
        print(host_name)
        host_img_url = event.host.profile.profile_image_storage_url

    no_user_img_icon_url = settings.MEDIA_URL + "no_photo_icon.jpg/"

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
                      "added_to_join_list": added_to_join_list,
                      "host_name": host_name,
                      "host_img_url": host_img_url,
                      "no_user_img_icon": no_user_img_icon_url,
                      }
    return render(request, "events/event_info.html", context_dict)

@login_required
def create_event(request):
    if request.method == "POST":
        #Reformat the start_time/end_time.
        #print("Request:", request.POST)
        #print("Files from form:", request.FILES)
        #print("Request:")
        #print(request.POST)
        #print(request.FILES)
        print("Startime: " + str(request.POST["start_time"]))
        updated_request_POST = request.POST.copy()
        start_date_datetime = datetime.strptime(str(request.POST["start_date"]), "%m-%d-%Y")
        start_time_datetime = datetime.strptime(str(request.POST["start_time"]), "%I:%M %p")
        end_date_datetime = datetime.strptime(str(request.POST["end_date"]), "%m-%d-%Y")
        end_time_datetime = datetime.strptime(str(request.POST["end_time"]), "%I:%M %p")
        updated_request_POST["start_date"] = str(start_date_datetime.date())
        updated_request_POST["start_time"] = str(start_time_datetime.time())
        updated_request_POST["end_date"] = str(end_date_datetime.date())
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
            user.add_to_hosting_list(event.event_id)
            return redirect("events:confirm_new_event", event_id=event.event_id)
        else:
            #print("FORM ERRORS:")
            #print("EVENT_FORM:")
            #print(event_form.errors)
            #print("IMAGE_FORM")
            #print(event_image_form.errors)
            #print("Location_form:")
            #print(location_form)
            return render(request, "events/new_event_form.html",
                          {"event_form": event_form, "event_image_form": event_image_form,
                           "location_form": location_form, })

    event_form = forms.EventForm()
    event_image_form = forms.EventImageForm()
    location_form = forms.LocationForm()
    return render(request, "events/new_event_form.html", {"event_form": event_form, "event_image_form": event_image_form,
                                                          "location_form": location_form,})

def edit_event(request):
    return render(request, "events/")

def confirm_new_event(request, event_id):
    event = Event.objects.filter(event_id=event_id)
    return render(request, "events/new_event_confirmation.html", {"event": event[0]})
