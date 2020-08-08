from django import forms

from address.models import AddressModel
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class AddressForm(forms.ModelForm):
    country = CountryField(blank_label='Choose your country').formfield()
    phone_number = PhoneNumberField(
        initial='+225',
        widget=PhoneNumberPrefixWidget(
            attrs={'placeholder': 'Phone number'}))

    class Meta:
        model = AddressModel
        fields = [
            'full_name', 'country', 'city', 'address_delivery',
            'address_type', 'postal_code', 'phone_number'
        ]


class AddressCheckoutForm(forms.ModelForm):
    country = CountryField(blank_label='Choose your country').formfield()
    phone_number = PhoneNumberField(
        initial='+225',
        widget=PhoneNumberPrefixWidget(
            attrs={'placeholder': 'Phone number'}))
    address_delivery = forms.CharField(
        label='Adresse delivery (optionnelle)',
        required=False, widget=forms.Textarea)

    class Meta:
        model = AddressModel
        fields = [
            'full_name', 'country', 'city',
            'postal_code', 'phone_number',
            'address_delivery'
        ]
