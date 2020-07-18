from django.urls import path
from payment.views import payment_method_view, payment_method_createview


app_name = 'payment'
urlpatterns = [
    path('process/', payment_method_view, name='method'),
    path('done/', payment_method_createview, name='endpoint'),
]
