from django import forms

from shop.models import ProductModel


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            'category', 'name', 'price',
            'label', 'desc', 'featured',
            'available', 'img', 'img_1',
            'img_2', 'img_3', 'img_4']

    def clean_price(self):
        price = self.fields['price']
        price = self.cleaned_data['price']
        if 99.99 <= price <= 1.00:
            raise forms.ValidationError(
                "Price must be greater than $1 or less than $100.")
        return price

    def clean_name(self):
        name = self.fields['name']
        name = self.cleaned_data['name']
        if len(name) >= 4:
            return name
        else:
            raise forms.ValidationError(
                "Product Name must be greater than 3 characters long.")
