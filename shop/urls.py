from django.urls import path
from django.views.generic import TemplateView
from shop.views import (
    SearchView, ProductListView,
    ProductDetailView, CategoryListView,
    CategoryDetailView, wishlist, addReview)

app_name = 'shop'
urlpatterns = [
    # url product
    path(
        'search/',
        SearchView.as_view(),
        name="search"),

    # url product
    path(
        'list/',
        ProductListView.as_view(
            extra_context={'page_title': 'All Products'}),
        name='all_product'),
    path(
        'detail/<slug>/',
        ProductDetailView.as_view(),
        name="product_detail"),

    # url category
    path(
        'category/list/',
        CategoryListView.as_view(
            extra_context={'page_title': 'All Category'}),
        name='all_category'),
    path(
        'category/detail/<slug>/', CategoryDetailView.as_view(),
        name='detail_category'),

    # URL wishlist
    path('wish/add/<int:product_id>/', wishlist, name='addwish'),
    path('wish/list/content/', TemplateView.as_view(
        extra_context={'page_title': 'Wish List'},
        template_name='shop/wishlist.html'), name='wishlist'),

    # URL compare
    path('compare/product/', TemplateView.as_view(
        extra_context={'page_title': 'Compare Product'},
        template_name='shop/compare.html'), name='compare'),

    # url review
    path('review/add/<slug>/', addReview, name='add_review'),
]
