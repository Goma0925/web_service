from django.shortcuts import render
from .models import *
from datetime import datetime
from django.core.paginator import Paginator

def eventboard(request):
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
    return render(request, "eventboard/eventboard.html", {"events": future_events, "page_range": page_range,
                                                     "current_page_num": current_page_num,
                                                     "page_has_previous": page_has_previous, "page_has_next": page_has_next
                                                    })

def event_page(request, event_id="default"):
    #event_id = request.GET.get('event_id', None)
    event = Event.objects.filter(event_id=event_id)
    return render(request, "eventboard/event_page.html", {"event": event[0], "event_tags": event[0].tags})