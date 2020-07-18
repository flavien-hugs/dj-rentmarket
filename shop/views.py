from django.urls import reverse
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect

from shop.forms import ReviewForm
from shop.models import (
    ProductModel, CategoryModel,
    ReviewModel, WishListModel)
from location.models import LocationModel

from analytics.mixins import ObjectViewMixin


# HOME
class HomeListView(ListView):
    model = ProductModel
    template_name = 'shop/index.html'

    def get_queryset(self):
        queryset = ProductModel.objects.get_available()[:3]
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'Accueil'
        return super().get_context_data(**kwargs)


# SEARCHVIEW
class SearchView(ListView):
    template_name = 'shop/products/product_list.html'
    success_url = reverse_lazy('shop:search')

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.request.GET.get('q')
        kwargs['page_title'] = 'Results search for : {}'.format(
            kwargs['query'])
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        request = self.request
        mdict = request.GET
        query = mdict.get('q', None)
        if query is not None:
            return ProductModel.objects.search(query)
        return ProductModel.objects.get_available()


# PRODUCT ALL
class ProductListView(ListView):
    model = ProductModel
    template_name = 'shop/products/product_list.html'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        kwargs['category'] = CategoryModel.objects.all()
        kwargs['products'] = self.get_queryset().prefetch_related('category')
        kwargs['page_title'] = 'Tous les produits'
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return ProductModel.objects.get_available()


# DETAIL PRODUIT
class ProductDetailView(ObjectViewMixin, DetailView):
    template_name = 'shop/products/product_detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return ProductModel.objects.get_available()

    def get_context_data(self, *args, **kwargs):
        kwargs['form'] = ReviewForm()
        kwargs['category'] = CategoryModel.objects.all()
        return super().get_context_data(*args, **kwargs)

        try:
            instance = ProductModel.objects.get(
                slug=slug, available=True)
        except ProductModel.DoesNotExist:
            raise Http404("Not found..")
        except ProductModel.MultipleObjectsReturned:
            qs = ProductModel.objects.filter(
                slug=slug, available=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm")
        return instance


class UserHistoryView(LoginRequiredMixin, ListView):
    template_name = "shop/products/user.history.html"

    def get_context_data(self, *args, **kwargs):
        location_obj, new_obj = LocationModel.objects.new_or_get(self.request)
        kwargs['location'] = location_obj
        return super().get_context_data(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(
            ProductModel, model_queryset=False)
        return views


# CATEGORY ALL
class CategoryListView(ProductListView):
    model = CategoryModel
    queryset = CategoryModel.objects.all()
    template_name = 'shop/products/product_list.html'

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = 'toutes les catégories'
        return super().get_context_data(**kwargs)


# DETAIL CATEGORY
class CategoryDetailView(DetailView):
    model = CategoryModel

    def get_context_data(self, **kwargs):
        self.obj = self.get_object()
        self.product_set = self.obj.productmodel_set.all()
        kwargs["product"] = self.product_set
        return super().get_context_data(**kwargs)


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
    product = get_object_or_404(ProductModel, slug=slug, available=True)
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
