from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


from shop.views import HomeListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('shop/', include('shop.urls', namespace='shop')),
    path('customer/', include('accounts.urls', namespace='accounts')),
    path('location/', include('location.urls', namespace='location')),
    path('order/', include('orders.urls', namespace='orders')),
    path('admin/', admin.site.urls),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
