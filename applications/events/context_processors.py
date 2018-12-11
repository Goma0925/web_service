from django.conf import settings

def debug_mode_flag(request):
    return {'DEBUG_MODE': settings.DEBUG}