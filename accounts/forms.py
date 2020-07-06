from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField


class SignUpForm(UserCreationForm):
    country = CountryField(blank_label='selectionner votre pays').formfield()
    city = forms.CharField(label='Ville', max_length=10, required=True)
    email = forms.EmailField(label='Email', max_length=50, required=True)
    phone_number = PhoneNumberField(label='Numéro de téléphone')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'country', 'city', 'phone_number',
            'password1', 'password2'
        )
        widgets = {'country': CountrySelectWidget()}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password2'])
        user.is_active = True

        if commit:
            user.save()
        return user


class UserInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
