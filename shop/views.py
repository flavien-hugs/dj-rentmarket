import random
from django.urls import reverse
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect

from shop.forms import ReviewForm
from shop.models import (
    ProductModel, MainCategoryModel, CategoryModel,
    ReviewModel, WishListModel)

from analytics.models import CategoryView
from analytics.mixins import ObjectViewMixin


# SEARCHVIEW
class SearchView(ListView):
    template_name = 'shop/products/product_list.html'
    success_url = reverse_lazy('shop:search')

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.request.GET.get('q', None)
        kwargs['page_title'] = 'Results were found for\
            the search for : {}'.format(kwargs['query'])
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is not None:
            return ProductModel.objects.search(query)
        return ProductModel.objects.get_available()


# PRODUCT ALL
class ProductListView(ListView):
    queryset = ProductModel.objects.get_available()
    template_name = 'shop/products/product_list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        kwargs['count'] = ProductModel.objects.get_available().count()
        return super().get_context_data(**kwargs)


# DETAIL PRODUIT
class ProductDetailView(ObjectViewMixin, DetailView):
    model = ProductModel
    template_name = 'shop/products/product_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['form'] = ReviewForm()
        kwargs['category'] = CategoryModel.objects.all()
        kwargs['page_title'] = self.object.name

        kwargs['related_product'] = sorted(
            ProductModel.objects.get_related(
                instance=self.get_object())[:25],
            key=lambda x: random.random())

        if self.request.user.is_authenticated:
            kwargs['history_product'] = sorted(
                self.request.user.objectviewedmodel_set.by_model(
                    ProductModel, model_queryset=False)[:25],
                key=lambda x: random.random())
        return super().get_context_data(**kwargs)


# CATEGORY LIST VIEW
class CategoryListView(ListView):
    queryset = CategoryModel.objects.all()
    paginate_by = 50
    template_name = 'shop/products/product_list.html'


# DETAIL CATEGORY VIEW
class CategoryDetailView(ObjectViewMixin, DetailView):
    model = CategoryModel
    template_name = 'shop/category/category_detail.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated or None:
            kwargs['new_view'] = CategoryView.objects.add_count(
                self.request.user, self.get_object())

        obj = self.get_object()
        kwargs['object_list'] = obj.productmodel_set.get_available()
        kwargs['product_count'] = kwargs['object_list'].count()

        kwargs['page_title'] = 'Category: {}'.format(
            self.object.name)
        return super().get_context_data(**kwargs)


# WISHLIST VIEWS
def wishlist(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        addwish = ProductModel.objects.create(
            pk=product_id, user=request.user)
        WishListModel.objects.get_or_create(wishlist=addwish)
        return HttpResponse("Success !")
    else:
        return HttpResponse("request method")


# REVIEW VIEW
def addReview(request, slug):
    product = get_object_or_404(ProductModel, slug=slug, available=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.user or None)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            ReviewModel.objects.get_or_create(
                product=product, rating=rating,
                name=name, email=email,
                comment=comment, date=timezone.now())

            return HttpResponseRedirect(
                reverse('shop:product_detail', args=(slug,)))

    return HttpResponse()
