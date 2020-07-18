from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path, include

from shop.views import HomeListView


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('shop/', include('shop.urls', namespace='shop')),
    path('customer/', include('accounts.urls', namespace='accounts')),
    path('location/', include('location.urls', namespace='location')),
    path('address/', include('address.urls', namespace='address')),
    path('order/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('subscribe/', include('subscription.urls', namespace='subscribe')),
    path('faq/', TemplateView.as_view(
        template_name='pages/faq.html'), name='faq'),
    path('cgu/', TemplateView.as_view(
        template_name='pages/cgu.html'), name='cgu'),
    path('contact/', TemplateView.as_view(
        template_name='pages/contact.html'), name='contact'),
    path('about/', TemplateView.as_view(
        template_name='pages/about.html'), name='about'),
    path('admin/', admin.site.urls),
]

handler404 = TemplateView.as_view(
    template_name='pages/erreurs/error404.html')

handler404 = TemplateView.as_view(
    template_name='pages/erreurs/error500.html')

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
