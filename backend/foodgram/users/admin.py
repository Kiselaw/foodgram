from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
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
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'username',
            'first_name',
            'last_name'
        )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'first_name',
                'last_name',
                'is_staff',
                'is_active',
                'is_superuser'
            )
        }
        ),
    )
