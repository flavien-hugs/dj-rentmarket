from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView


from orders.models import OrdersModel, OrderPurchaseModel


class OrderListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return OrdersModel.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):

    def get_object(self):
        qs = OrdersModel.objects.by_request(
            self.request).filter(
            order_id=self.kwargs.get('order_id')
                )
        if qs.count() == 1:
            return qs.first()
        raise Http404


class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'orders/library.html'

    def get_queryset(self):
        return OrderPurchaseModel.objects.product_by_request(self.request)


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            print(data)
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = OrderPurchaseModel.\
                    objects.product_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404
