from django.shortcuts import render
from .models import *
from datetime import datetime
from django.core.paginator import Paginator

def eventboard(request):
    #Sort by nearest upcoming events
    future_events = Event.objects.filter(date__gte=datetime.now())
    print("Num of events:", len(future_events))
    #May need revision here when num of events increased.
    for event in future_events:
        event.date = str(event.date.month) + "/" + str(event.date.day) + "/" + str(event.date.year)
        print(event.date)

    paginator = Paginator(future_events, 24)
    #https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    return render(request, "eventboard/index.html", {"events": future_events})