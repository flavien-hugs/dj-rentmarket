from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import SignUpForm, UserInfoUpdateForm
# Create your views here.


def signup(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""

    if request.user_agent.is_mobile:
        device_type = 'Mobile'
    if request.user_agent.is_tablet:
        device_type = 'Tablet'
    if request.user_agent.is_pc:
        device_type = 'PC'
    if request.user_agent.is_touch_capable:
        device_type = 'touch capable'
    if request.user_agent.is_bot:
        device_type = 'bot'

    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string

    device_family = request.user_agent.device.family

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(data=request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 'Super ! Votre compte a été créé avec succès !')
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
            print(form.errors)

    context = {
        'form': form,
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type": os_type,
        "os_version": os_version,
        "device_family": device_family
    }
    template = 'accounts/signup.html'
    return render(request, template, context)


@method_decorator(login_required, name='dispatch')
class AccountUpdateView(UpdateView):
    form_class = UserInfoUpdateForm
    template_name = "accounts/update.html"
    success_url = reverse_lazy('dashboard:dashboard')

    def get_object(self):
        return self.request.user


def deleteAccount(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('home')
