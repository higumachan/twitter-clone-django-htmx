from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth.admin import UserAdmin
from django.urls import NoReverseMatch
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from commons.admin import UserCreatedBaseModelAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # limit displayed fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = [field.name for field in LogEntry._meta.get_fields()]
    list_filter = ['user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    list_display = ['__str__', 'content_type', 'action_time', 'user', 'object_link']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        # only for superusers, cannot return False, the module
        # wouldn't be visible in admin
        return request.user.is_superuser and request.method != 'POST'

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                link = mark_safe('<a href="%s">%s</a>' % (
                                 reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                                         args=[obj.object_id]),
                                 escape(obj.object_repr),)
                                 )
            except NoReverseMatch:
                link = obj.object_repr
        return link
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')
