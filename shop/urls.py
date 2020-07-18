from django.urls import path
from django.views.generic import TemplateView
from shop.views import (
    SearchView, ProductListView, UserHistoryView,
    ProductDetailView, CategoryListView,
    wishlist, addReview)

app_name = 'shop'
urlpatterns = [
    # url product
    path('search/', SearchView.as_view(), name="search"),
    path('product/', ProductListView.as_view(), name='all_product'),
    path(
        'product/detail/<slug>/', ProductDetailView.as_view(),
        name="produit_detail"),
    path(
        'user/history/product/',
        UserHistoryView.as_view(),
        name='userhistory'),

    # url category
    path('category/', CategoryListView.as_view(), name='all_category'),
    path(
        'category/<slug>/', CategoryListView.as_view(),
        name='detail_category'),

    # URL wishlist
    path('addwish/<int:product_id>/', wishlist, name='addwish'),
    path('wishlist/', TemplateView.as_view(
        template_name='shop/wishlist.html'), name='wishlist'),
    # URL compare
    path('compare/', TemplateView.as_view(
        template_name='shop/compare.html'), name='compare'),

    # url review
    path('review/<slug>/', addReview, name='add_review'),
]
