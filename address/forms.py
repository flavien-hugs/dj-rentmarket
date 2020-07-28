from django import forms

from address.models import AddressModel
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField


class AddressForm(forms.ModelForm):
    country = CountryField(blank_label='Choose your country').formfield()
    country.widget.attrs.update({'class': 'form-control'})
    phone_number = PhoneNumberField(label='Phone Number')
    note = forms.CharField(required=False, widget=forms.Textarea)
    note.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = AddressModel
        fields = [
            'full_name', 'country', 'city', 'address_delivery',
            'address_type', 'postal_code', 'phone_number', 'note'
        ]


class AddressCheckoutForm(forms.ModelForm):
    country = CountryField(blank_label='Choose your country').formfield()
    country.widget.attrs.update({'class': 'form-control'})
    phone_number = PhoneNumberField(label='Phone Number')
    address_delivery = forms.CharField(
        label='Adresse delivery (optionnelle)',
        required=False, widget=forms.Textarea)
    address_delivery.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = AddressModel
        fields = [
            'full_name', 'country', 'city',
            'postal_code', 'phone_number',
            'address_delivery'
        ]
