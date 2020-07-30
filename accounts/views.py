from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import(
    DetailView, FormView, UpdateView, View, CreateView)
from django.shortcuts import render, redirect, get_object_or_404


from accounts.models import EmailActivationModel
from core.mixins import NextUrlMixin, RequestFormAttachMixin
from accounts.forms import(
    SignUpForm, LoginForm, GuestEmailForm,
    UserInfoUpdateForm, ReactivateEmailForm)

# GETTING MY MODEL USER
User = get_user_model()


class UserHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin, View):
    success_url = reverse_lazy('accounts:login')
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            q = EmailActivationModel.objects.filter(
                key__iexact=key)
            cqs = q.confirmed()

            if cqs.count() == 1:
                obj = cqs.first()
                obj.activate()
                messages.success(
                    request,
                    "Your email has been confirmed. Please login.")
                return redirect('accounts:login')
            else:
                aqc = q.filter(activated=True)
                if aqc.exists():
                    reset_link = reverse('accounts:password_reset')
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('accounts:login')

        context = {'form': self.get_form(), 'key': key}
        template = 'accounts/activation-error.html'
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        messages.success(self.request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivationModel.objects.email_exists(email).first()
        new_activation = EmailActivationModel.objects.create(
            user=obj.user, email=email)
        new_activation.send_token_activation()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        template = 'accounts/activation-error.html'
        return render(self.request, template, context)


class GuestSignUpView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = GuestEmailForm
    default_next = reverse_lazy('accounts:signup')

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'accounts/login.html'
    default_next = reverse_lazy('dashboard:dashboard')

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:verify')


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserInfoUpdateForm
    template_name = "accounts/update.html"
    success_url = reverse_lazy('dashboard:dashboard')

    def get_object(self):
        return self.request.user


def deleteAccount(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('home')
