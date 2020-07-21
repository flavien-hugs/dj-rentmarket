from django.urls import path

from dashboard.views import(
    ManageProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView)

app_name = 'dashboard'
urlpatterns = [
    path('', ManageProductListView.as_view(
        extra_context={'page_title': 'Dashboard'}
        ), name='dashboard'),
    path('create/', ProductCreateView.as_view(
        extra_context={'page_title': 'Add product'}
        ), name='add_product'),
    path('edit/<slug>/', ProductUpdateView.as_view(
        extra_context={'page_title': 'Update product'}
        ), name='update_product'),
    path('delete/<pk>/', ProductDeleteView.as_view(
        extra_context={'page_title': 'Delete product'}
        ), name='delete_product'),
]
