from django.urls import path

from dashboard.views import(
    ManageProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView)

app_name = 'dashboard'
urlpatterns = [
    path('', ManageProductListView.as_view(), name='dashboard'),
    path('create/', ProductCreateView.as_view(), name='add_product'),
    path('edit/<slug>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
