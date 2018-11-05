from django.shortcuts import render
from .models import *
from datetime import datetime

def eventboard(request):
    #Sort by nearest upcoming events
    future_events = Event.objects.filter(date__gte=datetime.now())
    print("Num of events:", len(future_events))
    for event in future_events:
        event.date = str(event.date.month) + "/" + str(event.date.day) + "/" + str(event.date.year)
        print(event.date)

    return render(request, "eventboard/index.html", {"events": future_events})