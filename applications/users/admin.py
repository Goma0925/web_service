from applications.users import models
#from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

"""
    ModelAdmin is how you customize its appearance.
"""

#admin.site.site_header("Unnamed Webservice")
#admin.site.site_title("Administrator site")
#admin.site.index_title("I")


@admin.register(models.User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')
    list_filter = ["is_staff"]
    search_fields = ("email", "username")
