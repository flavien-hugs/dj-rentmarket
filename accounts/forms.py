from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class SignUpForm(UserCreationForm):
    country = CountryField(blank_label='selectionner votre pays').formfield()
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'country', 'password1', 'password2')
        widgets = {
            'country': CountrySelectWidget()
        }


class UserInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
