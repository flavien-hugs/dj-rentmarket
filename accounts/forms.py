from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import(
    authenticate, login, get_user_model)

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField

from accounts.models import EmailActivationModel, GuestEmailModel

# GETTING MY MODEL USER
User = get_user_model()


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        queryset = EmailActivationModel.objects.email_exists(email)
        if not queryset.exists():
            register_link = reverse('accounts:signup')
            message = """This email does not exists, would you like to <a href="{link}">signup</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(message))
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse("accounts:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.""".format(resend_link=link)
                confirm_email = EmailActivationModel.objects.filter(
                    email=email)
                is_confirmed = confirm_email.confirmed().exists()
                if is_confirmed:
                    msg1 = "Please check your email to\
                    confirm your account or " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivationModel\
                    .objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed." + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmed and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Please check your email,\
                it is valid ?")
        login(request, user)
        self.user = user
        return data


class SignUpForm(forms.ModelForm):
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
            'full_name', 'email',
            'country', 'city', 'phone_number',
            'password1', 'password2'
        )
        widgets = {'country': CountrySelectWidget()}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'country', 'phone_number']

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password1 != password1:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            'full_name', 'email',
            'password', 'is_active', 'admin'
        ]

    def clean_password(self):
        return self.initial["password"]


class UserInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'full_name', 'phone_number',
            'country', 'city', 'email']


class GuestEmailForm(forms.ModelForm):
    class Meta:
        model = GuestEmailModel
        fields = ['email']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        if commit:
            obj.save()
            self.request.session['guest_email_id'] = obj.id
        return obj
