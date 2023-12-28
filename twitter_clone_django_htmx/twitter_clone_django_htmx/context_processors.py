from typing import Dict
from django.http.request import HttpRequest
from django.conf import settings


def global_view_additional_context(_: HttpRequest) -> Dict:
    """
    context defined here is provided additionally to the template rendering context
    """
    context = {
        'URL_PREFIX': settings.URL_PREFIX,
        'STATIC_URL': settings.STATIC_URL,
    }
    return context
