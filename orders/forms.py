from django import forms
from django.forms import TextInput

from orders.models import OrdersModel
from django_countries.fields import CountryField


class OrdersForm(forms.ModelForm):
    country = CountryField(blank_label='selectionner votre pays').formfield()
    country.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = OrdersModel
        fields = [
            'first_name', 'last_name', 'company', 'country',
            'address', 'apartement', 'city', 'zipcode', 'email',
            'phone', 'note'
        ]

        widgets = {
            'note': TextInput(attrs={'class': 'form-control'}),
        }
