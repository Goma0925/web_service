from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', "location", "host_name", "host")

@admin.register(models.Location)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('location_name',)