from django.urls import path

from shop.views import HomeListView, ProductDetailView, CategoryListView

app_name = 'shop'
urlpatterns = [
    # url product
    path('', HomeListView.as_view(), name="home"),
    path('product/detail/<slug>/', ProductDetailView.as_view(),name="produit_detail"),
    # url category
    path('category/', CategoryListView.as_view(), name='all_category_list'),
    path('category/<slug>/', CategoryListView.as_view(), name='detail_category'),
]
