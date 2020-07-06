from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    date_hierarchy = 'date_joined'
    list_display = (
        'first_name', 'email', 'country',
        'phone_number', 'date_joined', 'is_active')
    list_filter = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('personal info', {'fields': (
            'first_name', 'phone_number', 'country',
            'city', 'date_joined', 'is_active')}),
        ('permissions', {'fields': ('admin',)}),)

    add_fieldsets = (
            (None, {
                'classes': ('wide', 'extrapretty'),
                'fields': ('email', 'password1', 'password2')}),)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.unregister(Group)
