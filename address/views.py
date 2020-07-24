from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.http import is_safe_url

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView


from payment.models import PaymentModel
from address.models import AddressModel
from address.forms import AddressCheckoutForm, AddressForm


class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'address/list.html'

    def get_queryset(self):
        request = self.request
        payment, payment_created = PaymentModel.objects.new_or_get(request)
        return PaymentModel.objects.filter(payment=payment)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'address/update.html'
    form_class = AddressForm
    success_url = reverse_lazy('address:address-update')

    def get_queryset(self):
        payment, payment_created = PaymentModel.objects.new_or_get(
            self.request)
        return PaymentModel.objects.filter(payment=payment)


class AddressCreateView(LoginRequiredMixin, CreateView):
    template_name = 'address/update.html'
    form_class = AddressForm
    success_url = reverse_lazy('address:address-create')

    def form_valid(self, form):
        payment, payment_created = PaymentModel.objects.new_or_get(
            self.request)
        instance = form.save(commit=False)
        instance.payment = payment
        instance.save()
        return super().form_valid(form)


def checkout_address_create_view(request):
    form = AddressCheckoutForm(request.POST or None)
    context = {"form": form}
    print(context)

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        instance = form.save(commit=False)
        payment, payment_created = PaymentModel.objects.new_or_get(request)
        if payment is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.payment = payment
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")
        else:
            print("Error here")
            return redirect("location:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect("location:checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == "POST":
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            payment, payment_created = PaymentModel.objects.new_or_get(request)
            if shipping_address is not None:
                qs = AddressModel.objects.filter(
                    payment=payment, id=shipping_address)
                if qs.exists():
                    request.session[
                        address_type + "_address_id"] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect('location:checkout')
