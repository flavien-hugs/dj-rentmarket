from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import(
    UserHomeView, AccountEmailActivateView, LoginView,
    SignUpView, GuestSignUpView, AccountUpdateView,
    deleteAccount)

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeView, PasswordChangeDoneView)

app_name = 'accounts'
urlpatterns = [
    path('account/', UserHomeView.as_view(
        extra_context={'page_title': 'Account'}),
        name='account'),

    path('account/signup/', SignUpView.as_view(), name='signup'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),

    path('account/update/', AccountUpdateView.as_view(
        extra_context={'page_title': 'Change Your Account Detail'}),
        name='update'),

    path(
        'account/signup/guest/',
        GuestSignUpView.as_view(), name='guest'),

    path(
        'account/email/confirm/<key>/',
        AccountEmailActivateView.as_view(), name='email-activate'),

    path(
        'account/email/resend-activation/',
        AccountEmailActivateView.as_view(), name='resend-activation'),

    path('account/compte/<int:pk>/delete/', deleteAccount, name='delete'),

    path(
        'account/password/password/change/',
        PasswordChangeView.as_view(
            extra_context={'page_title': 'Password Change'},
            template_name='accounts/password_change_form.html'),
        name='password_change'),

    path(
        'account/password/password/done/',
        PasswordChangeDoneView.as_view(
            extra_context={'page_title': 'Password Change Done'},
            template_name='accounts/password_change_done.html'),
        name='password_change_done'),

    path('account/password/reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_email.txt'
        ), name='password_reset'),

    path(
        'account/password/reset/done/',
        PasswordResetDoneView.as_view(
            extra_context={'page_title': 'Password Reset Done'},
            template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    path(
        'account/password/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            extra_context={'page_title': 'Password Reset Confirm'},
            template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),

    path(
        'account/password/reset/complete/',
        PasswordResetCompleteView.as_view(
            extra_context={'page_title': 'Password Reset Complete'},
            template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

]
