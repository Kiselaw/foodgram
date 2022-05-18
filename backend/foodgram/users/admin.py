from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    list_display = (
        'id', 'email', 'username',
        'first_name', 'last_name',
        'is_staff', 'is_active',
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
