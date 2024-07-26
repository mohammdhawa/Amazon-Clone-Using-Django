from .models import Settings


def get_settings_context(request):
    data = Settings.objects.last()

    return {'settings_data': data}
