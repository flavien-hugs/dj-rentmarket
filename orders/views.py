from django.shortcuts import render, redirect, reverse

from orders.forms import OrdersForm
from location.location import Location
from orders.models import ItemOrderModel


# Create your views here.

def create_order(request):
    location = Location(request)
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in location:
                ItemOrderModel.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'])
            location.clear_session()
            request.session['id_order'] = order.id
            return redirect(reverse('shop:home'))
    else:
        form = OrdersForm()

    context = {'location': location, 'form': form}
    template = 'orders/orders_create.html'
    return render(request, template, context)
