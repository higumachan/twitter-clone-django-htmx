import logging

from django.contrib import admin
from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)


class UserCreatedBaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):  # type: ignore
        has_created_by = any(True for f in obj._meta.get_fields() if f.name == "created_by")
        if obj._state.adding and has_created_by:
            obj.created_by = request.user
        has_updated_by = any(True for f in obj._meta.get_fields() if f.name == "updated_by")
        if has_updated_by:
            obj.updated_by = request.user

        obj.save()

    def save_formset(self, request, form, formset, change):  # type: ignore
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            has_created_by = any(True for f in instance._meta.get_fields() if f.name == "created_by")
            if instance._state.adding and has_created_by:
                instance.created_by = request.user  # only update created_by once!
            has_updated_by = any(True for f in instance._meta.get_fields() if f.name == "updated_by")
            if has_updated_by:
                instance.updated_by = request.user
            instance.save()
        formset.save_m2m()


admin.site.unregister(Group)  # remove Group from admin
