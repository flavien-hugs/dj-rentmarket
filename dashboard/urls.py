from django.urls import path

from dashboard.views import(
    ManageProductListView, ProductCreateView,
    ProductUpdateView, ProductDeleteView)

app_name = 'dashboard'
urlpatterns = [
    # url product
    #  path('', UserDashboardProductView.as_view(
    #     template_name='dashboard/dashboard.html'),
    #     name="dashboard"),
    # path('create-product/', createProduct, name='add-product'),
    # path(
    # 'delete-product/<int:product>/', deleteProduct, name='delete-product'),

    path('', ManageProductListView.as_view(), name='dashboard'),
    path('create/', ProductCreateView.as_view(), name='add_product'),
    path('edit/<slug>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<pk>/', ProductDeleteView.as_view(), name='delete_product'),
]
