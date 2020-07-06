from django import forms
from subscription.models import SubscribeModel


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribeModel
        fields = ['email']
