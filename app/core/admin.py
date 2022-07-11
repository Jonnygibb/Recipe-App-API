"""
Django admin customisation.
"""
from django.contrib import admin
# Rename of user admin to prevent confusion with custom user model.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Allows for translation using django languages.
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    # Define which fields display and where on the page.
    fieldsets = (
        (
            None,
            {
                'fields':
                (
                    'email',
                    'password'
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields':
                (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields':
                (
                    'last_login',
                )
            }
        ),
    )
    readonly_fields = ['last_login']

    # Fieldsets for the add user admin page.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields':
                (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            }
        ),
    )


admin.site.register(models.User, UserAdmin)
