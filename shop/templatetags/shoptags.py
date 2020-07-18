import random
from django import template
from shop.models import ProductModel, ReviewModel

register = template.Library()


@register.inclusion_tag('shop/products/sidebar_latest_product.html')
def show_latest_product(count=20):
    latest_product = ProductModel.objects.filter(
        available=True,
        pub_date__isnull=False,
        ).order_by('-pub_date')[:count]
    context = {'latest_product': latest_product}
    return context


@register.inclusion_tag('shop/products/featured/featured_product.html')
def show_featured_product(count=100):
    featured_product = ProductModel.objects.featured().filter(
       pub_date__isnull=False).order_by('-pub_date')[:count]
    context = {'featured': featured_product}
    return context


@register.inclusion_tag('shop/products/similar_product.html')
def show_similar_product(self, count=20):
    product = ProductModel.objects.get_available()
    product_similar = sorted(
        (product).prefetch_related('category').distinct()[:count],
        key = lambda x: random.random())
    context = {'product_similar': product_similar}
    return context


@register.inclusion_tag('shop/review/review_list.html')
def show_review_list(count):
    review_list = ReviewModel.objects.order_by('-date')[:count]
    context = {'review_list': review_list}
    return context


@register.simple_tag(takes_context=True)
def departments_opened(context, name):

    if context['request'].resolver_match.url_name == name:
        return 'departments--opened departments--fixed'

    return ''
