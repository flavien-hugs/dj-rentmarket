from django.views.generic import ListView, DetailView

from shop.models import ProductModel, CategoryModel


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# CATEGORY ALL
class CategoryListView(ListView):
    model = CategoryModel
    template_name = 'shop/all_category_list.html'

    def get_queryset(self):
        category = CategoryModel.objects.all()
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'toutes les catégories'
        return context
