from django import forms

from shop.models import ProductModel


class ProductModelModelForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = '__all__'
