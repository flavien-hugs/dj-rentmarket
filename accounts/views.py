from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import SignUpForm, UserInfoUpdateForm
# Create your views here.


def signup(request):

    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(
                request, email=user.email, password=raw_password)
            login(request, user)
            messages.success(
                request, 'Super ! Votre compte a été créé avec succès !')
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
            print(form.errors)

    context = {'form': form}
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
