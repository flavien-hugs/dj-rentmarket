from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

from shop.forms import ReviewForm
from shop.models import (
    ProductModel, CategoryModel,
    ReviewModel, ImageModel, WishListModel)


@require_http_methods(["GET"])
def search(request):
    products = ProductModel.objects.filter(
        available=True).order_by('-rent_date')
    try:
        q, price = request.GET.get('q'), request.GET.get('price')
    except:
        q = price = None

    if q or price:
        products = products.filter(
            Q(name__icontains=q) |
            Q(category__name__icontains=q)
        ).distinct()
        products = products.order_by('-price')
    else:
        return redirect('shop:search')

    context = {'products': products, 'query': q, 'query': price}
    template = 'shop/category/category_list.html'
    return render(request, template, context)


# HOME
class HomeListView(ListView):
    model = ProductModel
    template_name = 'shop/index.html'

    def get_queryset(self):
        queryset = ProductModel.objects.filter(available=True)[:3]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'accueil'
        return context


# DETAIL PRODUIT
class ProductDetailView(DetailView):
    Model = ProductModel
    template_name = 'shop/products/product_detail.html'

    def get_queryset(self):
        queryset = ProductModel.objects.filter(available=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = CategoryModel.objects.all()
        images = ImageModel.objects.all()
        form = ReviewForm()
        context['category'] = category
        context['images'] = images
        context['form'] = form
        return context


# PRODUCT ALL
class ProductListView(ListView):
    model = ProductModel
    template_name = 'shop/category/category_list.html'
    paginate_by = 30

    def get_queryset(self):
        return ProductModel.objects.filter(
            available=True).order_by('-price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = CategoryModel.objects.all()
        products = ProductModel.objects.filter(
            available=True).prefetch_related('category')
        context['category'] = category
        context['products'] = products
        context['page_title'] = 'tous les produits'
        return context


# CATEGORY ALL
class CategoryListView(ProductListView):
    model = CategoryModel
    template_name = 'shop/category/category_list.html'
    paginate_by = 30

    def get_queryset(self):
        return CategoryModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'toutes les catégories'
        return context


# WishList
def wishlist(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        user = request.GET['user']
        addwish = ProductModel.objects.create(
            pk=product_id, user=user)
        wish = WishListModel(wishlist=addwish)

        wish.save()

        return HttpResponse("Success !")
    else:
        return HttpResponse("request method")


# Review VIEW
def addReview(request, slug):
    product = get_object_or_404(
        ProductModel, slug=slug, available=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']
            review = ReviewModel()
            review.product = product
            review.rating = rating
            review.name = name
            review.email = email
            review.comment = comment
            review.date = timezone.now()
            review.save()

            return HttpResponseRedirect(
                reverse('shop:produit_detail', args=(slug,)))

    else:
        form = ReviewForm()

    return HttpResponse()
