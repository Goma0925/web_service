from django.conf import settings
from django.db import models
import datetime
import os
from random import randint
import string
from imagekit.models import ImageSpecField
from imagekit.processors import crop

class Location(models.Model):
    location_name = models.CharField(max_length=90, blank=False)
    slug = models.SlugField(max_length=255, null=True)
    #address

    def set_location_name(self, location_name):
        self.location_name = location_name

    def __str__(self):
        return str(self.location_name)

class Event(models.Model):
    event_id = models.CharField(default="XXXXXXXXXX", max_length=10, blank=False, unique=True)
    name = models.CharField(max_length=150, blank=False)
    date = models.DateField(default=datetime.date.today, blank=False)
    start_time = models.TimeField(default=None, blank=False)
    end_time = models.TimeField(default=None, blank=False)
    picture = models.ImageField(upload_to = 'event_images/', default="place_holders/place_holder_700x400.png")
    language = models.CharField(default="English", max_length=50, blank=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False)
    description = models.CharField(max_length=160, blank=False)
    tags = models.CharField(default="", max_length=50, blank=False) #String of tags splitted by ","
    host_name = models.CharField(max_length=160, default="", blank=False)
    """↑Will Update: Delete"""
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    #slug = models.SlugField(max_length=255, null=True)##WHat's this?



    def create_event(self, name, date, start_time, end_time, location, description, host_name, host):
        #self.event_id = #
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.description = description
        self.host_name = host_name
        """↑Will Update"""
        self.host = None

    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename)

    # def issue_page_id(self):
        #ID collision detection needed
    #     page_id = ""
    #     for i in range(10):
    #         if randint(0, 1) == 0:
    #             page_id += str(random(0,9))
    #         else:
    #             page_id += string.ascii_uppercase
    #     return page_id


    def __str__(self):
        return str(self.name)
