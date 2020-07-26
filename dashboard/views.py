from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import(
    ListView, CreateView, UpdateView, DeleteView)
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import(
    LoginRequiredMixin, PermissionRequiredMixin)

from shop.models import ProductModel
from orders.models import OrdersModel
from accounts.mixins import UserAccountMixin
from dashboard.forms import ProductModelModelForm

# GETTING MY MODEL USER
User = get_user_model()


class GetContextData(object):

    def get_context_data(self, **kwargs):
        kwargs['product_count'] = ProductModel.objects.get_available(
            ).filter(user=self.request.user).count()

        kwargs['order_count'] = OrdersModel.objects.by_request(
            self.request).count()
        return super().get_context_data(**kwargs)


class UserMixin(UserAccountMixin, object):
    def get_object(self):
        return self.get_account()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.get_object())


class UserEditeMixin(UserAccountMixin, object):

    def form_valid(self, form):
        message = """Product update successful !"""
        messages.success(self.request, message)
        form.instance.user = self.get_account()
        return super().form_valid(form)


class UserProductMixin(UserEditeMixin):
    model = ProductModel


class UserProductEditMixin(UserProductMixin, UserEditeMixin):
    form_class = ProductModelModelForm
    template_name = 'dashboard/d_form.html'
    success_url = reverse_lazy('dashboard:dashboard')


class UserProductDetailRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(ProductModel, pk=kwargs['slug'])
        return obj.get_absolute_url()


# USER MANAGE PRODUCT
class ManageProductListView(UserProductMixin, GetContextData, ListView):
    template_name = 'dashboard/dashboard.html'

    def queryset(self):
        return ProductModel.objects.get_available(
            ).filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        kwargs['orders'] = OrdersModel.objects.by_request(
            self.request)
        return super().get_context_data(**kwargs)


# USER ORDER LIST
class UserOrderListView(LoginRequiredMixin, GetContextData, ListView):
    template_name = 'dashboard/d_user_order.html'

    def get_queryset(self):
        return OrdersModel.objects.by_request(self.request)


# USER PRODUCT LIST
class UserProductListView(LoginRequiredMixin, GetContextData, ListView):
    template_name = 'dashboard/d_user_product.html'

    def get_queryset(self):
        return ProductModel.objects.get_available(
            ).filter(user=self.request.user)


# USER PRODUCT CREATE VIEW
class ProductCreateView(PermissionRequiredMixin, UserProductEditMixin, CreateView):
    permission_required = 'product.add_product'


# USER PRODUCT UPDATE VIEW
class ProductUpdateView(PermissionRequiredMixin, UserProductEditMixin, UpdateView):
    template_name = 'dashboard/d_form.html'
    permission_required = 'product.update_product'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Update product: %s' % self.object.name
        return super().get_context_data(**kwargs)


# USER PRODUCT DELETE VIEW
class ProductDeleteView(PermissionRequiredMixin, UserProductEditMixin, DeleteView):
    template_name = 'dashboard/d_delete.html'
    permission_required = 'product.delete_product'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Delete product : {}'.format(
            str(self.object.name))
        return super().get_context_data(**kwargs)
