import os
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

import stripe
from payment.models import PaymentModel, CardModel

STRIPE_SECRET_KEY = os.environ.get(
    'STRIPE_SECRET_KEY',
    "sk_test_51H6F3bEVRs2R6z6LBLDgt4mlR50t4QHqDGb1BJ1A7NII7ejhXPVMlA9tnlWMy8WWtPjrQrtXeHBRcsfXdJwjmQL700iWChY2Zj")

STRIPE_PUB_KEY = os.environ.get(
    'STRIPE_PUB_KEY',
    'pk_test_51H6F3bEVRs2R6z6LE0qO5BL9PAOYUPwRS0EI5TOnNd3P0hI5y4GAPTb47uSGT7rbE7tmua6qcjbreOpSVMop4pLh00BH4DVIcg')
stripe.api_key = STRIPE_SECRET_KEY


def payment_method_view(request):
    payment, payment_created = PaymentModel.objects.new_or_get(request)
    if not payment:
        return redirect("location:location")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next

    context = {
        "publish_key": STRIPE_PUB_KEY,
        "next_url": next_url,
        'page_title': 'payment'}
    template = 'payment/payment-method.html'
    return render(request, template, context)


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        payment, payment_created = PaymentModel.objects.new_or_get(request)
        if not payment:
            return HttpResponse(
                {"message": "Cannot find this user"},
                status_code=401)
        token = request.POST.get("token")
        if token is not None:
            new_card_obj = CardModel.objects.add_new(
                payment, token)
            print(new_card_obj)
        return JsonResponse(
            {"message": "Success! Your card was added."})
    return HttpResponse("error", status_code=401)
