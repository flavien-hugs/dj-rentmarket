from django import forms

from shop.models import ReviewModel

RATING = (
    (1, 'une étoile'),
    (2, 'deux étoiles'),
    (3, 'trois étoiles'),
    (4, 'quatres étoiles'),
    (5, 'cinq étoiles'),
)


class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        label='Votre note', choices=RATING, required=True)

    class Meta:
        model = ReviewModel
        fields = ['rating', 'name', 'email', 'comment']
