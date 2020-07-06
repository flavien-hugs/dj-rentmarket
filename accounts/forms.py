from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import(
    UserCreationForm, AuthenticationForm, ReadOnlyPasswordHashField)


from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField

# GETTING MY MODEL USER
User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Adresse email', max_length=50, required=True)
    country = CountryField(blank_label='selectionner votre pays').formfield()
    city = forms.CharField(label='Ville', max_length=10, required=True)
    phone_number = PhoneNumberField(label='Numéro de téléphone')
    password1 = forms.CharField(
        label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='confirm password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name',
            'country', 'city', 'phone_number',
            'password1', 'password2'
        )
        widgets = {'country': CountrySelectWidget()}

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AuthenticateForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['email', 'password']


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    phone_number = PhoneNumberField(label='Téléphone')

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'is_active']

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            'email', 'password', 'phone_number',
            'country', 'is_active', 'admin']

    def clean_password(self):
        return self.initial['password']


class UserInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'phone_number', 'country', 'city', 'email']
