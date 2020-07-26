from django.urls import path
from django.views.generic import TemplateView

from location.views import(
    location_home, location_update,
    checkout_home)

app_name = 'location'

urlpatterns = [
    path('cart/content/', location_home, name='detail'),
    path('update/', location_update, name='update'),
    path('checkout/success/', TemplateView.as_view(
        extra_context={'page_title': 'Checkout Done'},
        template_name='location/checkout_done.html'),
        name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('track/', TemplateView.as_view(
        extra_context={'page_title': 'Track Product'},
        template_name='location/track_location.html'),
        name='track'),
]
