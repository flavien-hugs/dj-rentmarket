from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import(
    LoginRequiredMixin, PermissionRequiredMixin)

from shop.models import ProductModel
from orders.models import OrdersModel


class UserMixin(object):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class UserEditeMixin(object):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserProductMixin(LoginRequiredMixin, UserMixin, UserEditeMixin):
    model = ProductModel
    fields = '__all__'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductModel.objects.all().count()
        orders = OrdersModel.objects.all().count()
        context['count_products'] = products
        context['count_orders'] = orders
        return context


class UserProductEditMixin(UserProductMixin, UserEditeMixin):
    fields = '__all__'
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'dashboard/dashboard_product_form.html'


class ManageProductListView(UserProductMixin, ListView):
    template_name = 'dashboard/dashboard.html'


class ProductCreateView(PermissionRequiredMixin, UserProductEditMixin, CreateView):
    permission_required = 'product.add_product'


class ProductUpdateView(PermissionRequiredMixin, UserProductEditMixin, UpdateView):
    permission_required = 'product.update_product'


class ProductDeleteView(PermissionRequiredMixin, UserProductEditMixin, DeleteView):
    template_name = 'dashboard/delete_product.html'
    success_url = reverse_lazy('dashboard:dashboard')
    permission_required = 'product.delete_product'
