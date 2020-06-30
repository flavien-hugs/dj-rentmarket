from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from shop.models import ProductModel
from cart.forms import CartProductForm
# Create your views here.


@require_POST
def addLocation(request, id_product):
    cart = Cart(request)
    product = get_object_or_404(ProductModel, id=id_product)
    cart_product_form = CartProductForm(request.POST)

    if cart_product_form.is_valid():
        cd = cart_product_form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )
        return redirect('cart:detail_location')


def removeLocation(request, id_produit):
    cart = Cart(request)
    produit = get_object_or_404(ProductModel, id=id_produit)
    cart.remove(produit)
    return redirect('cart:detail_location')


def detailLocation(request):
    cart = Cart(request)
    for item in cart:
        item['form_update_quantity'] = CartProductForm(
            initial={'quantity': item['quantity'], 'update': True})

    context = {'cart': cart}
    template = 'cart/location_detail.html'
    return render(request, template, context)
