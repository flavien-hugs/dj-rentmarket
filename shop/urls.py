from django.urls import path

from shop.views import (
    search, ProductListView,
    ProductDetailView, CategoryListView)

app_name = 'shop'
urlpatterns = [
    # url product
    path('search/', search, name="search"),
    path('product/', ProductListView.as_view(), name='all_product'),
    path('product/detail/<slug>/',
        ProductDetailView.as_view(), name="produit_detail"),
    # url category
    path('category/', CategoryListView.as_view(), name='all_category'),
    path('category/<slug>/', CategoryListView.as_view(),
        name='detail_category'),
]
