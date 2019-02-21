from django.conf import settings
from applications.events.forms import SearchForm

def debug_mode_flag(request):
    return {'DEBUG_MODE': settings.DEBUG}

def search_form(request):
    search_form = SearchForm()
    return {"search_form": search_form}
