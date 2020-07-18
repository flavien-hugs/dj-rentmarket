from django import forms
from subscription.models import SubscribeModel


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribeModel
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_base, provider = email.split("@")
        domain, extension = provider.split('.')
        if not extension == "edu":
            raise forms.ValidationError(
                "Please use a valid .edu email address")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('name')
        return full_name
