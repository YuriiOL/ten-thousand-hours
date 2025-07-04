from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ['email']}),
        (_('Info'), {'fields': ['name']}),
        (
            _('Permissions'),
            {
                'fields': [
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ]
            }
        ),
        (_('Last Login'), {'fields': ['last_login']}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'fields': [
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            ]
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Timer)
