from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    list_display = (
        'email', 'username',
        'first_name', 'last_name',
        'is_staff', 'is_active',
        'link',
    )
    list_editable = (
        'email', 'username',
        'first_name', 'last_name',
        'is_staff', 'is_active',
    )
    list_filter = (
        'email', 'username',
        'first_name', 'last_name',
        'is_staff', 'is_active',
    )
    list_display_links = ('link',)


admin.site.register(CustomUser, CustomUserAdmin)
