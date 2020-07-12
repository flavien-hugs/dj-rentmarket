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
    date_hierarchy = 'joined'
    list_display = (
        'first_name', 'last_name', 'email', 'country',
        'phone_number', 'joined', 'is_active')
    list_filter = ('joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('personal info', {'fields': (
            'first_name', 'last_name', 'phone_number', 'country',
            'city', 'is_active')}),
        ('permissions', {'fields': ('admin',)}),)

    add_fieldsets = (
            (None, {
                'classes': ('wide', 'extrapretty'),
                'fields': ('email', 'password1', 'password2')}),)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.unregister(Group)
