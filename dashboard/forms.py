from django.forms import ModelForm, FileField, FileInput

from shop.models import ProductModel


class ProductModelModelForm(ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            'category', 'name', 'price',
            'label', 'desc', 'featured', 'available']

    img = FileField(
        widget=FileInput(attrs={'multiple': 'true'}))
