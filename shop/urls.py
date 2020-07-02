from django.urls import path

from shop.views import (
    search, HomeListView,
    ProductDetailView, CategoryListView)

app_name = 'shop'
urlpatterns = [
    # url product
    path('', HomeListView.as_view(), name="home"),
    path('search/', search, name="search"),
    path('product/detail/<slug>/',
        ProductDetailView.as_view(), name="produit_detail"),
    # url category
    path('category/', CategoryListView.as_view(), name='all_category'),
    path('category/<slug>/', CategoryListView.as_view(),
        name='detail_category'),
]
