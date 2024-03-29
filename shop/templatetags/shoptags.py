from django import template

from shop.models import ProductModel, ReviewModel

register = template.Library()


@register.inclusion_tag('shop/products/sidebar_latest_product.html')
def show_latest_product(count=20):
    latest_product = ProductModel.objects.filter(
        available=True, pub_date__isnull=False,
        ).order_by('-pub_date').distinct()[:count]
    context = {'latest_product': latest_product}
    return context


@register.inclusion_tag('shop/review/review_list.html')
def show_review_list(count=5):
    review_list = ReviewModel.objects.order_by('-rating')[:count]
    context = {'review_list': review_list}
    return context


@register.simple_tag(takes_context=True)
def departments_opened(context, name):

    if context['request'].resolver_match.url_name == name:
        return 'departments--opened departments--fixed'

    return ''
