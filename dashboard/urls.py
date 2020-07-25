from django.urls import path
from django.views.generic.base import RedirectView
from dashboard.views import(
    UserProductListView, ManageProductListView, ProductCreateView,
    UserOrderListView, ProductUpdateView, ProductDeleteView)

app_name = 'dashboard'
urlpatterns = [
    path('', ManageProductListView.as_view(
        extra_context={'page_title': 'Dashboard'}
        ), name='dashboard'),
    path('user/product/list/', UserProductListView.as_view(
        extra_context={'page_title': 'Your products List'}),
        name='user_product'),
    path(
        'vendor/', RedirectView.as_view(
            pattern_name='dashboard:user_product'),
        name='product_list'),
    path('user/order/list/', UserOrderListView.as_view(
        extra_context={'page_title': 'Your orders List'}),
        name='user_order'),
    path('create/product/', ProductCreateView.as_view(
        extra_context={'page_title': 'Add New Product'}),
        name='add_product'),
    path(
        'edit/product/<slug>/',
        ProductUpdateView.as_view(), name='update_product'),
    path(
        'delete/product/<slug>/',
        ProductDeleteView.as_view(), name='delete_product'),
]
