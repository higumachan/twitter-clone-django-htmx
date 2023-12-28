from django.contrib import admin

from twitter.models import Tweet


# Register your models here.

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
