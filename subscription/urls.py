from django.urls import path

from subscription.views import subscribeView

app_name = 'subscribe'

urlpatterns = [
    path('', subscribeView, name='subscribe'),
]
