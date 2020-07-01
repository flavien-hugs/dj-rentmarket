from django.urls import path

from location.views import detailLocation, addLocation, removeLocation

app_name = 'location'

urlpatterns = [
    path('detail/', detailLocation, name='detail'),
    path('add/<int:product>/', addLocation, name='add'),
    path('remove/<int:product>/', removeLocation, name='remove'),
]
