from django.conf import settings
from django.db import models
import datetime
import os

class Location(models.Model):
    location_name = models.CharField(max_length=30, blank=False)
    #address

    def set_location_name(self, location_name):
        self.location_name = location_name

    def __str__(self):
        return str(self.location_name)

class Event(models.Model):
    name = models.CharField(max_length=30, blank=False)
    date = models.DateField(default=datetime.date.today, blank=False)
    start_time = models.TimeField(default=None, blank=False)
    end_time = models.TimeField(default=None, blank=False)
    #picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)


    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False)
    description = models.CharField(max_length=160, blank=False)
    host_name = models.CharField(default="", max_length=160, blank=False)
    """↑Update: Delete"""
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    # upload_to = Define a key word of where to store the image in POST request.
    #profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def create_event(self, name, date, start_time, end_time, location, description, host_name, host):
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description
        self.host_name = host_name
        """Update"""
        self.host = None

    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)

    def is_in_future(self):
        pass

    def __str__(self):
        return str(self.name)


