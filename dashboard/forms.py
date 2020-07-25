from django import forms

from shop.models import ProductModel


class ProductModelModelForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            'category', 'name', 'price',
            'label', 'desc', 'featured', 'available']

    img = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': 'true'}))

    def clean(self, **kwargs):
        return super().clean(**kwargs)

    def clean_price(self):
        price = self.cleaned_data('price')
        if 99.99 <= price <= 1.00:
            raise forms.ValidationError(
                "Price must be greater than $1 or less than $100.")
        return price

    def clean_name(self):
        name = self.cleaned_data('name')
        if len(name) >= 4:
            return name
        else:
            raise forms.ValidationError(
                "Producr Name must be greater than 3 characters long.")
