"""twitter_clone_django_htmx URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


# update displayed header/title
admin.site.site_header = settings.SITE_HEADER
admin.site.site_title = settings.SITE_TITLE

urlpatterns = [
    path('admin/', admin.site.urls),
]
