
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CodeVaultUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined',
        'last_login',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'date_joined',
        'last_login',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    readonly_fields = (
        'last_login',
        'date_joined',
    )


admin.site.unregister(User)
admin.site.register(User, CodeVaultUserAdmin)
