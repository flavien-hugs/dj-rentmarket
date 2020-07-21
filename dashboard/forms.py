from django import forms

from shop.models import ProductModel


class ProductModelModelForm(forms.ModelForm):
    user = forms.ModelChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = ProductModel.objects.filter(
            user=self.request.user)

    class Meta:
        model = ProductModel
        fields = '__all__'
