from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
