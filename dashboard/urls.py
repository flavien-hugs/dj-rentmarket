from django.urls import path

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
    path('user/order/list/', UserOrderListView.as_view(
        extra_context={'page_title': 'Your orders List'}),
        name='user_order'),
    path('create/', ProductCreateView.as_view(
        extra_context={'page_title': 'Add New Product'}),
        name='add_product'),
    path('edit/<slug>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<slug>/', ProductDeleteView.as_view(), name='delete_product'),
]
