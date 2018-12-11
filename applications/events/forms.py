from django import forms
from .models import Event
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import datetime, date

today = str(date.today()).replace("-", "/")

class EventForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        print("Type cleaned_data:", type(cleaned_data))
        print("cleaned_data:", cleaned_data)
        print("cleaned date - date", cleaned_data["date"])
        print("cleaned date - date", cleaned_data["start_time"])
        print("cleaned date - date", cleaned_data["end_time"])
        return cleaned_data
    class Meta(): #Configures the model to work with
        model = Event
        fields = ("name", "date", "start_time", "end_time", "language",  "location", "description", "tags")
        widgets = {'date': DatePickerInput(options={
                       # "min": today
                    }),
                   "description": forms.Textarea(),
                   'start_time': TimePickerInput(options={
                       "format": 'hh:mm a',
                       "stepping": 15,
                   }).start_of('Event time'),
                   'end_time': TimePickerInput(options={
                       "format": 'hh:mm a',
                       "stepping": 15
                   }).end_of('Event time'),
                   }
        help_text = {
            "start_time": "Please clear the end time before you change the start time",
        }


