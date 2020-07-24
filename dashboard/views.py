from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import(
    ListView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import(
    LoginRequiredMixin, PermissionRequiredMixin)

from shop.models import ProductModel
from orders.models import OrdersModel
from dashboard.forms import ProductModelModelForm


class UserMixin(object):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_object(self):
        return self.request.user


class UserEditeMixin(object):

    def form_valid(self, form):
        message = """Product update successful !"""
        messages.success(self.request, message)
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserProductMixin(LoginRequiredMixin, UserEditeMixin):
    model = ProductModel


class UserProductEditMixin(UserProductMixin, UserEditeMixin):
    form_class = ProductModelModelForm
    template_name = 'dashboard/d_form.html'
    success_url = reverse_lazy('dashboard:dashboard')


class ManageProductListView(UserProductMixin, ListView):
    model = ProductModel
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs['product_count'] = ProductModel.objects.get_available(
            ).filter(user__in=[self.request.user]).count()

        kwargs['order_count'] = OrdersModel.objects.by_request(
            self.request).count()
        kwargs['orders'] = OrdersModel.objects.by_request(self.request)
        return super().get_context_data(**kwargs)


class UserOrderListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/d_user_order.html'

    def get_queryset(self):
        return OrdersModel.objects.by_request(self.request)

    def get_context_data(self, **kwargs):
        kwargs['count'] = OrdersModel.objects.by_request(
            self.request).count()
        return super().get_context_data(**kwargs)


class UserProductListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/d_user_product.html'

    def get_queryset(self):
        return ProductModel.objects.get_available(
            ).filter(user__in=[self.request.user])

    def get_context_data(self, **kwargs):
        kwargs['count'] = ProductModel.objects.get_available(
            ).filter(user__in=[self.request.user]).count()
        return super().get_context_data(**kwargs)


class ProductCreateView(PermissionRequiredMixin, UserProductEditMixin, CreateView):
    permission_required = 'product.add_product'


class ProductUpdateView(PermissionRequiredMixin, UserProductEditMixin, UpdateView):
    template_name = 'dashboard/d_form.html'
    permission_required = 'product.update_product'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Update product: %s' % self.object.name
        return super().get_context_data(**kwargs)


class ProductDeleteView(PermissionRequiredMixin, UserProductEditMixin, DeleteView):
    template_name = 'dashboard/d_delete.html'
    permission_required = 'product.delete_product'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Delete product : %s' % self.object.name
        return super().get_context_data(**kwargs)
