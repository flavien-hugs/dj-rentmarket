from django.shortcuts import render, redirect, get_object_or_404

from shop.models import ProductModel
from location.location import Location


# Create your views here.*
def addLocation(request, product):
    location = Location(request)
    product = get_object_or_404(ProductModel, id=product)
    location.add(product=product)

    return redirect('location:detail')


def removeLocation(request, product):
    location = Location(request)
    product = get_object_or_404(ProductModel, id=product)
    location.remove(product)
    return redirect('location:detail')


def detailLocation(request):
    location = Location(request)
    template = 'location/location_detail.html'
    context = {'location': location, 'page_title': 'location'}
    return render(request, template, context)
