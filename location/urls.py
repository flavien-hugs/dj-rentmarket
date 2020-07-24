from django.urls import path
from django.views.generic import TemplateView

from location.views import(
    location_home, location_update,
    checkout_home, checkout_done)

app_name = 'location'

urlpatterns = [
    path('cart/content/', location_home, name='detail'),
    path('update/', location_update, name='update'),
    path('checkout/success/', checkout_done, name='success'),
    path('checkout/', checkout_home, name='checkout'),
    path('track/', TemplateView.as_view(
        template_name='location/track_location.html'),
        name='track'),
]
