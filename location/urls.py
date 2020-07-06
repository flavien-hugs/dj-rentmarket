from django.urls import path
from django.views.generic import TemplateView
from location.views import detailLocation, addLocation, removeLocation

app_name = 'location'

urlpatterns = [
    path('panier/', detailLocation, name='detail'),
    path('add/<int:product>/', addLocation, name='add'),
    path('remove/<int:product>/', removeLocation, name='remove'),
    path('track/', TemplateView.as_view(
        template_name='location/track_location.html'),
        name='track'),
]
