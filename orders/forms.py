from django import forms

from orders.models import OrdersModel
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField


class OrdersForm(forms.ModelForm):
    order_id = forms.CharField(required=False, widget=forms.HiddenInput)
    country = CountryField(blank_label='selectionner votre pays').formfield()
    country.widget.attrs.update({'class': 'form-control'})
    phone_number = PhoneNumberField(label='Numéro de téléphone')
    note = forms.CharField(required=False, widget=forms.Textarea)
    note.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = OrdersModel
        fields = '__all__'
