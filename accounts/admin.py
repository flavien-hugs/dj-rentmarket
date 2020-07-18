from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.forms import UserAdminChangeForm, UserAdminCreationForm
from accounts.models import GuestEmailModel, EmailActivationModel

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    date_hierarchy = 'joined'
    list_display = (
        'full_name', 'email', 'country',
        'phone_number', 'joined', 'is_active')
    list_filter = ('joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('personal info', {'fields': (
            'full_name', 'phone_number', 'country',
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


@admin.register(EmailActivationModel)
class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = EmailActivationModel


@admin.register(GuestEmailModel)
class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = GuestEmailModel
