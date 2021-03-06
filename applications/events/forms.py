#Django libs
from django import forms
from applications.events.models import Event, Location
from applications.users.models import User
from django.conf import settings
#Python libs
import random
import string
import datetime
from PIL import Image
import os
#Other additional libs
from bootstrap_datepicker_plus import DateTimePickerInput

timeTuples = ('00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30', '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30')

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.issued_event_id = "XXXXXXXXXX"
        super(EventForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        :param commit: Wheather or not to commit to the DB
        :return: event obj
                This method is responsible for issuing event_id and cropping the image and saving it in MEDIA DIR.
        """
        #Issue a new event ID. Bind this form to the ID.
        if self.issued_event_id == "XXXXXXXXXX":
            event_id_issued_successfully = False
            while not event_id_issued_successfully:
                event_id = self.generate_event_id()
                if not Event.objects.filter(event_id=event_id).exists(): # Check if this checks for the duplicates
                    self.issued_event_id = event_id
                    event_id_issued_successfully = True
        if commit:
            event = super().save(commit=False)
            event.event_id = self.issued_event_id
            event = super().save(commit=True)
        else:
            event = super().save(commit=False)
        event.event_id = self.issued_event_id
        return event
        # except Exception as e:
        #     print("save() ERROR!!!")
        #     print(str(e))

    def generate_event_id(self):
        event_id = ""
        for i in range(10):
            if random.randint(0, 1) == 0:
                event_id += str(random.randint(0, 9))
            else:
                event_id += random.choice(string.ascii_uppercase)
        return event_id

    class Meta(): #Configures the model to work with
        model = Event
        fields = ("name",  "start_date", "end_date", "start_time", "end_time", "language", "description", "tags",)
        widgets = {
                   "description": forms.Textarea(),
                   "start_time": forms.Select(),
                   "end_time": forms.Select(),
                   }
        # help_text = {
        #     "start_time": "Please clear the end time before you change the start time",
        # }

class EventEditForm(forms.ModelForm):
    class Meta(): #Configures the model to work with
        model = Event
        fields = ("name",  "start_date", "end_date", "start_time", "end_time", "language", "description", "tags",)
        widgets = {
                   "description": forms.Textarea(),
                   "start_time": forms.Select(),
                   "end_time": forms.Select(),
                   }

class LocationForm(forms.ModelForm):
    class Meta(): #Configures the model to work with
        model = Location
        fields = ("location_name", "address")


class EventImageForm(forms.Form):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    image = forms.ImageField()
    def save_image_of(self, event):
        img_format = ".jpg"
        stored_time = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        #print("time format:", stored_time)
        #print("cleaned_date:", self.cleaned_data)
        image_x = self.cleaned_data.get('x')
        image_y = self.cleaned_data.get('y')
        image_width = self.cleaned_data.get('width')
        image_height = self.cleaned_data.get('height')
        #print("Coordinates:", image_x, image_y, image_width, image_height)
        # Resize the image and store it in media dir.
        image = Image.open(self.cleaned_data.get('image')).convert('RGB')  # event.image
        cropped_image = image.crop((image_x, image_y, image_width + image_x, image_height + image_y))
        resized_image = cropped_image.resize((700, 400), Image.ANTIALIAS)

        file_name = event.event_id + "_" + stored_time + img_format
        image_storage_path = os.path.join(settings.MEDIA_ROOT, settings.HANGOUT_IMAGE_DIR, file_name)
        image_storage_url = settings.MEDIA_URL + settings.HANGOUT_IMAGE_URL + file_name + "/"
        try:
            print("Saving img at PATH:", image_storage_path)
            print("Saving img at URL:", image_storage_url)
            resized_image.save(image_storage_path, format="JPEG")  # Image.save() saves the image in a file at the given path(event.image.path)
        except Exception:
            raise forms.ValidationError("This type of image file cannot be used.")
        return str(image_storage_url)


class BookmarkRequestForm(forms.Form):
    bookmark_request = forms.CharField(widget=forms.HiddenInput)
    def request_type(self):
        return self.cleaned_data.get('bookmark_request')

class SearchForm(forms.Form):
    search_string = forms.CharField()
