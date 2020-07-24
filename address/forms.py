from django import forms

from address.models import AddressModel
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField


class AddressForm(forms.ModelForm):
    country = CountryField(blank_label='selectionner votre pays').formfield()
    country.widget.attrs.update({'class': 'form-control'})
    phone_number = PhoneNumberField(label='Numéro de téléphone')
    note = forms.CharField(required=False, widget=forms.Textarea)
    note.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = AddressModel
        fields = [
            'full_name', 'country', 'city', 'address_delivery',
            'address_type', 'zipcode', 'phone_number', 'note'
        ]


class AddressCheckoutForm(forms.ModelForm):
    country = CountryField(blank_label='selectionner votre pays').formfield()
    country.widget.attrs.update({'class': 'form-control'})
    phone_number = PhoneNumberField(label='Numéro de téléphone')
    note = forms.CharField(required=False, widget=forms.Textarea)
    note.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = AddressModel
        fields = [
            'full_name', 'country', 'city', 'address_delivery',
            'address_type', 'zipcode', 'phone_number', 'note'
        ]
