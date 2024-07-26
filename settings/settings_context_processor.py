from .models import Settings
from django.core.cache import cache


def get_settings_context(request):

    data = cache.get('settings_data')
    if data is None:
        # If the data doesn't exist in the cache, retrieve it from the data source
        data = Settings.objects.last()
        # Cache the data for future use
        cache.set('settings_data', data, timeout=60*60*24)

    context = {'settings_data': data}

    return context
