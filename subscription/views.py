from django.contrib import messages
from django.shortcuts import render

from subscription.forms import SubscribeForm
from subscription.models import SubscribeModel
from subscription.emails import send_multiple_email


# Create your views here.


def subscribeView(request):
    form = SubscribeForm()
    if request.method == 'POST':
        form = SubscribeForm(data=request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            if SubscribeModel.objects.filter(email=form.email).exists():
                messages.warning(
                    request, "your Email is already exists in our database")
            else:
                form.save()
                messages.warning(
                    request, 'your email is already added to our database')
                send_multiple_email(form.email)

    context = {'form': form}
    template = "newsletter/subscribe.html"
    return render(request, template, context)
