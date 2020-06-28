from django.views.generic import ListView, DetailView

from shop.models import Product


# HOME
class HomeListView(ListView):
    model = Product
    template_name = 'index.html'

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)[:3]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'accueil'
        return context


# DETAIL PRODUIT
# class ProductDetailView(DetailView):
#     pass
