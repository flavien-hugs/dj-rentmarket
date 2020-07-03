from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods

from shop.models import ProductModel, CategoryModel, ImageModel


@require_http_methods(["GET"])
def search(request):
    category = CategoryModel.objects.all()
    products = ProductModel.objects.filter(
        available=True).prefetch_related('category')
    try:
        q = request.GET.get('q')
    except:
        q = None

    if q:
        products = products.filter(
            Q(name__icontains=q)
        ).distinct()
        category = CategoryModel.objects.all()
    else:
        return redirect('shop:search')

    context = {'category': category, 'products': products, 'query': q}
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
        context['category'] = category
        context['images'] = images
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
