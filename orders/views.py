from django.shortcuts import render, redirect, reverse

from orders.forms import OrdersForm
from location.location import Location
from orders.models import ItemOrderModel


# Create your views here.
def create_order(request):
    location = Location(request)
    form = OrdersForm()
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in location:
                ItemOrderModel.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'])

            # clear location
            location.clear_session()

            # set the order in the session
            request.session['order_id'] = order.id

            # redirect for home
            return redirect(reverse('home'))

    context = {'form': form}
    template = 'orders/orders_create.html'
    return render(request, template, context)
