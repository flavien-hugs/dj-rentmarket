from django.urls import path

from address.views import(
    AddressListView,
    AddressUpdateView,
    AddressCreateView,
    checkout_address_create_view,
    checkout_address_reuse_view)


app_name = 'address'

urlpatterns = [
    path('', AddressListView.as_view(), name='address'),
    path('create/', AddressCreateView.as_view(), name='address-create'),

    path('<pk>/update/', AddressUpdateView.as_view(), name='address-update'),
    path(
        'checkout/address/create/',
        checkout_address_create_view,
        name='checkout_address_create'),

    path(
        'checkout/address/reuse/',
        checkout_address_reuse_view,
        name='checkout_address_reuse'),
]
