from django.shortcuts import render
from .models import *
from datetime import datetime
from django.core.paginator import Paginator
from . import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import random
from . import views_support_script
from django.contrib.auth.decorators import login_required


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
    #event_id = request.GET.get('event_id', None)
    event = Event.objects.filter(event_id=event_id)
    return render(request, "events/event_info.html", {"event": event[0], "event_tags": event[0].tags})

@login_required
def create_event(request):
    if request.method == "POST":
        print("Request:" + str(request.POST))
        form = forms.EventForm(request.POST)
        x = input("Before validation.")
        if form.is_valid():
            event = form.save(commit=False)
            user = request.user
            event.host = user
            event_id = views_support_script.generate_event_id()
            event_id_issued_successfully = False
            while not event_id_issued_successfully:
                try:
                    event.event_id = event_id
                    event.save()
                    event_id_issued_successfully = True #Check if this checks for the duplicates
                except:
                    event_id = views_support_script.generate_event_id()
            event.save()
            return render(request, "events/create_event_confirmation.html")
        else:
            print("form invalid.")
    event_form = forms.EventForm()
    #event_form.fields['date'].widget = DatePickerInput()
    #event_form.fields['start_time'].widget = TimePickerInput()
    #event_form.fields['end_time'].widget = TimePickerInput()
    return render(request, "events/create_event.html", {"event_form": event_form})

