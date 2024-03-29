import random
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect

from shop.forms import ReviewForm
from shop.recommender import Recommender
from analytics.models import CategoryView
from analytics.mixins import ObjectViewMixin

from shop.models import (
    ProductModel, CategoryModel, ReviewModel, WishListModel)


class ProductViewCounter(object):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs['slug']
        url = get_object_or_404(ProductModel, slug=slug, available=True)
        session_key = 'vues_{}'.format(url.pk)
        if not self.request.session.get(session_key, False):
            url.views = F('views') + 1
            url.save()
            self.request.session[session_key] = True
        return super().get_redirect_url(*args, **kwargs)


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
    paginate_by = 100
    queryset = ProductModel.objects.get_available()
    template_name = 'shop/products/product_list.html'

    def get_context_data(self, **kwargs):
        kwargs['count'] = ProductModel.objects.get_available().count()
        return super().get_context_data(**kwargs)


# DETAIL PRODUIT
class ProductDetailView(ObjectViewMixin, ProductViewCounter, DetailView):
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

        r = Recommender()
        kwargs['recommender'] = r.suggest_products(
            [self.object], 10)
        print(kwargs['recommender'])

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
def wishlist(request, slug):
    product = get_object_or_404(ProductModel, slug=slug, available=True)
    if request.method == 'POST':
        product = request.GET['product_id']
        addwish = ProductModel.objects.create(pk=product, user=request.user)
        WishListModel.objects.get_or_create(wishlist=addwish)
        return HttpResponse("Success !")
    return HttpResponse("request method")


# REVIEW VIEW
def addReview(request, slug):
    product = get_object_or_404(ProductModel, slug=slug, available=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            ReviewModel.objects.create(
                product=product, rating=rating,
                name=name, email=email,
                comment=comment, date=timezone.now())
            return HttpResponseRedirect(
                reverse('shop:product_detail', args=(slug,)))
    return HttpResponse("request method")
