from django.urls import path

from orders.views import(
    OrderListView, OrderDetailView,
    VerifyOwnership, LibraryView)

app_name = 'orders'
urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path(
        'endpoint/verify/ownership/', VerifyOwnership.as_view(),
        name='verify-ownership'),
    path('detail/<order_id>/', OrderDetailView.as_view(), name='detail'),
    path('library/', LibraryView.as_view(), name='library'),
]
