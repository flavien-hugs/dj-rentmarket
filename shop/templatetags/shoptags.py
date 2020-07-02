from django import template

from ..models import ProductModel

register = template.Library()


@register.inclusion_tag('shop/products/sidebar_latest_product.html')
def show_latest_product(count=20):
    latest_product = ProductModel.objects.filter(
        available=True,
        pub_date__isnull=False,
        ).order_by('-pub_date')[:count]
    context = {'latest_product': latest_product}
    return context


@register.inclusion_tag('shop/products/featured_product.html')
def show_featured_product(count=20):
    featured_product = ProductModel.objects.filter(
        available=True, pub_date__isnull=False
        ).order_by('-pub_date')[:count]
    context = {'featured_product': featured_product}
    return context


@register.inclusion_tag('shop/products/similar_product.html')
def show_similar_product(count=20):
    product = ProductModel.objects.filter(available=True)
    product_similar = product.prefetch_related('category')[:count]
    context = {'product_similar': product_similar}
    return context
