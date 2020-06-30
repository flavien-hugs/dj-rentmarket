from django import forms

CHOIX_QUANTITE_PRODUITS = [(i, str(i)) for i in range(1, 11)]


# Formulaire d'ajout de produit au panier
class CartProductForm(forms.Form):
    date_location = forms.DateField(
        label='Date de location',
        required=True,
        widget=forms.SelectDateWidget)

    quantite = forms.TypedChoiceField(
        error_messages={'required': 'Please enter a number'},
        choices=CHOIX_QUANTITE_PRODUITS,
        coerce=int,
        label='Quantity')

    update = forms.BooleanField(
        required=False, initial=False,
        widget=forms.HiddenInput)
