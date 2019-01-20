from django import forms
from applications.events.models import Event, Location
from applications.users.models import User
from django.conf import settings
from bootstrap_datepicker_plus import DateTimePickerInput
import random
import string
from PIL import Image
import os
from applications.events.models import HANGOUT_IMAGE_DIR


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
        fields = ("name",  "start_date", "end_date","start_time", "end_time", "language", "description", "tags",)
        widgets = {
                   "description": forms.Textarea(),
                   'start_time': DateTimePickerInput(options={
                       "format": 'hh:mm a',
                       "stepping": 15,
                   }).start_of('Event time'),
                   'end_time': DateTimePickerInput(options={
                       "format": 'hh:mm a',
                       "stepping": 15
                   }).end_of('Event time'),
                   }
        help_text = {
            "start_time": "Please clear the end time before you change the start time",
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
        #print("cleaned_date:", self.cleaned_data)
        image_x = self.cleaned_data.get('x')
        image_y = self.cleaned_data.get('y')
        image_width = self.cleaned_data.get('width')
        image_height = self.cleaned_data.get('height')
        #print("Coordinates:", image_x, image_y, image_width, image_height)
        # Resize the image and store it in media dir.
        image = Image.open(self.cleaned_data.get('image'))  # event.image
        cropped_image = image.crop((image_x, image_y, image_width + image_x, image_height + image_y))
        resized_image = cropped_image.resize((700, 400), Image.ANTIALIAS)
        image_storage_path = os.path.join(settings.MEDIA_ROOT, HANGOUT_IMAGE_DIR, event.event_id)
        image_storage_url = settings.MEDIA_URL + HANGOUT_IMAGE_DIR + event.event_id + "/"
        try:
            resized_image.save(image_storage_path, format="JPEG")  # Image.save() saves the image in a file at the given path(event.image.path)
        except Exception:
            raise forms.ValidationError("This type of image file cannot be used.")
        return str(image_storage_url)


class BookmarkRequestForm(forms.Form):
    bookmark_request = forms.CharField(widget=forms.HiddenInput)
    def request_type(self):
        return self.cleaned_data.get('bookmark_request')