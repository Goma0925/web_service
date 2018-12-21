from django.contrib import admin
from applications.events import models

# Register your models here.
@admin.register(models.Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', "location", "host_name", "host")
    search_fields = ("name", )

@admin.register(models.Location)
class LocationModelAdmin(admin.ModelAdmin):
    list_display = ('location_name',)
    search_fields = ("location_name",)
