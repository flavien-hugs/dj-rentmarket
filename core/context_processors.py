from location.location import Location
from shop.models import CategoryModel, ProductModel


def location(request):
    return {'location': Location(request)}


def category(request):
    nav = CategoryModel.objects.all()
    popular = ProductModel.objects.filter(available=True)

    return {'nav': nav, 'popular': popular}
