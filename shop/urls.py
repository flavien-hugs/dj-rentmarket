from django.urls import path

from shop.views import HomeListView

app_name = 'shop'
urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    # path('<slug>/', ProductDetailView.as_view(), name="produit_detail"),
]
