from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import(
    LoginRequiredMixin, PermissionRequiredMixin)

from shop.models import ProductModel
# from orders.models import OrdersModel


class UserMixin(object):
    def get_queryset(self):
        queryset = super(UserMixin, self).get_queryset()
        return queryset.filter(user=self.request.user)


class UserEditeMixin(object):
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserEditeMixin, self).form_valid(form)


class UserProductMixin(UserMixin, LoginRequiredMixin):
    model = ProductModel
    fields = [
        'category', 'name', 'slug', 'label', 'desc', 'img1', 'img2',
        'img3', 'img4', 'img5', 'price', 'available',
        'rent_date', 'keywords']

    success_url = reverse_lazy('dashboard:dashboard')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     orders = OrdersModel.objects.all().count()

    #     context['user'] = self.request.user
    #     context['total_orders'] = orders
    #     return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.order_by(
    #         '-pub_date').filter(products__in=[self.request.user])


class UserProductEditMixin(UserProductMixin, UserEditeMixin):
    fields = [
        'category', 'name', 'slug', 'label', 'desc', 'img1', 'img2',
        'img3', 'img4', 'img5', 'price', 'available',
        'rent_date', 'keywords']
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


# def createProduct(request):
#     form = ProductModelModelForm(instance=request.user)
#     if request.method == 'POST':
#         form = ProductModelModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard:dashboard')
#     else:
#         form = ProductModelModelForm()

#     context = {'form': form}
#     template = 'dashboard/dashboard_product_form.html'
#     return render(request, template, context)


# # HOME CREATE DELETE ORDER
# def deleteProduct(request, product):
#     product = get_object_or_404(ProductModel, id=product)
#     product.delete()
#     return redirect('dashboard:dashboard')
