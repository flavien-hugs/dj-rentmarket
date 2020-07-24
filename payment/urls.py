from django.urls import path
from payment.views import payment_method_view, payment_method_createview


app_name = 'payment'
urlpatterns = [
    path('process/', payment_method_view, name='method'),
    path('process/done/', payment_method_createview, name='done'),
]
