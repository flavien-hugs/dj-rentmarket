from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

import stripe
from shop.models import ProductModel
from orders.models import OrdersModel
from payment.models import PaymentModel
from address.models import AddressModel
from location.models import LocationModel
from address.forms import AddressCheckoutForm
from accounts.forms import LoginForm, GuestEmailForm

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_51H6F3bEVRs2R6z6LBLDgt4mlR50t4QHqDGb1BJ1A7NII7ejhXPVMlA9tnlWMy8WWtPjrQrtXeHBRcsfXdJwjmQL700iWChY2Zj")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_51H6F3bEVRs2R6z6LE0qO5BL9PAOYUPwRS0EI5TOnNd3P0hI5y4GAPTb47uSGT7rbE7tmua6qcjbreOpSVMop4pLh00BH4DVIcg')
stripe.api_key = STRIPE_SECRET_KEY


def location_detail_api_view(request):
    location_obj, new_obj = LocationModel.objects.new_or_get(request)
    product = [
        {
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name,
            "price": x.price
        }
        for x in location_obj.product.all()
    ]

    location_data = {
        "product": product,
        "total": location_obj.total
    }
    return JsonResponse(location_data)


def location_home(request):
    location_obj, new_obj = LocationModel.objects.new_or_get(request)
    context = {'location': location_obj, 'page_title': 'Location'}
    template = "location/location_detail.html"
    return render(request, template, context)


def location_update(request):
    product_id = request.POST.get('product_id')

    if product_id is not None:
        try:
            product_obj = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("location:detail")
        location_obj, new_obj = LocationModel.objects.new_or_get(request)
        if product_obj in location_obj.product.all():
            location_obj.product.remove(product_obj)
            added = False
        else:
            location_obj.product.add(product_obj)
            added = True
        request.session['location_items'] = location_obj.product.count()
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "LocationItemCount": location_obj.product.count()
            }
            return JsonResponse(json_data, status=200)

    return redirect("location:detail")


def checkout_home(request):
    location_obj, location_created = LocationModel.objects.new_or_get(request)
    order_obj = None
    if location_created or location_obj.product.count() == 0:
        return redirect('location:detail')

    login_form = LoginForm(request=request)
    guest_form = GuestEmailForm(request=request)
    address_form = AddressCheckoutForm()
    billing_address_id = request.session.get(
        "billing_address_id", None)

    shipping_address_id = request.session.get("shipping_address_id", None)

    payment, payment_created = PaymentModel.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if payment is not None:
        if request.user.is_authenticated:
            address_qs = AddressModel.objects.filter(
                payment=payment)
        order_obj, order_obj_created = OrdersModel.objects.new_or_get(
            payment, location_obj)
        if shipping_address_id:
            order_obj.shipping_address = AddressModel.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = AddressModel.objects.get(id=billing_address_id) 
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = payment.has_card

    if request.method == "POST":
        "check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = payment.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['location_items'] = 0
                del request.session['location_id']
                if not payment.user:
                    '''is this the best spot?'''
                    payment.set_card_inactive()
                return redirect("location:success")
            else:
                print(crg_msg)
                return redirect("location:checkout")
    context = {
        'page_title': 'Checkout',
        "object": order_obj,
        "payment": payment,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }

    return render(request, "location/checkout.html", context)


def checkout_done(request):
    return render(request, "location/checkout-done.html", {})
