from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse

from subscription.forms import SubscribeForm


def subscribeView(request):
    form = SubscribeForm(request.POST or None)
    if form.is_valid():
        if request.is_ajax():
            return JsonResponse({'message': 'Thank you for your submission'})

    if form.errors:
        errors = form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(
                errors, status=400,
                contont_type='application/json')
    context = {'form': form, 'title': 'Contact-Us'}
    template = "newsletter/subscribe.html"
    return render(request, template, context)
