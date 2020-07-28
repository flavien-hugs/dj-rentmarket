from django import forms

from shop.models import ProductModel, ProductImageModel


class ProductImageModelForm(forms.ModelForm):

    class Meta:
        model = ProductImageModel
        fields = ['img']


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            'category', 'name', 'price',
            'label', 'desc', 'featured', 'available']

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
