from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import handler404, handler500

from core.sitemaps import(
    StaticViewSitemap, CategorySitemapView,
    ProductSitemapView)

handler404 = core.views.handler404
handler500 = core.views.handler500

sitemaps = {
    'static': StaticViewSitemap,
    'category': CategorySitemapView,
    'product': ProductSitemapView,
}


urlpatterns = [
    path('', TemplateView.as_view(
        template_name='shop/index.html'), name='home'),
    path('product/', include('shop.urls', namespace='shop')),
    path('customer/', include('accounts.urls', namespace='accounts')),
    path('location/', include('location.urls', namespace='location')),
    path('address/', include('address.urls', namespace='address')),
    path('order/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('subscribe/', include('subscription.urls', namespace='subscribe')),
    path('faq/', TemplateView.as_view(
        extra_context={'page_title': 'Frequently Asked Questions'},
        template_name='pages/faq.html'), name='faq'),
    path('cgu/', TemplateView.as_view(
        extra_context={'page_title': 'Terms And Conditions'},
        template_name='pages/cgu.html'), name='cgu'),
    path('contact/', TemplateView.as_view(
        extra_context={'page_title': 'Contact Us'},
        template_name='pages/contact.html'), name='contact'),
    path('about/', TemplateView.as_view(
        extra_context={'page_title': 'About Us'},
        template_name='pages/about.html'), name='about'),
    path('delivery/', TemplateView.as_view(
        extra_context={'page_title': 'Delivery Information'},
        template_name='pages/delivery.html'), name='delivery'),
    path(
        'sitemap.xml',
        sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('xxx/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
