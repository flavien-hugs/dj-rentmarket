from django.urls import path

from cart.views import addLocation, removeLocation, detailLocation

app_name = 'cart'

urlpatterns = [
    path('', detailLocation, name="detail"),
    path('add/<int:id_produit>/', addLocation, name="add"),
    path('remove/<int:id_produit>/', removeLocation, name="remove"),
]
