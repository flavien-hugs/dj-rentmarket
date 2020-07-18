from django.urls import path
from django.contrib.auth.views import (
    LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView,
    PasswordChangeDoneView)


from accounts.views import(
    UserHomeView, AccountEmailActivateView, LoginView,
    SignUpView, GuestSignUpView, AccountUpdateView, deleteAccount)

app_name = 'accounts'
urlpatterns = [
    path('account/', UserHomeView.as_view(), name='account'),
    path('account/signup/', SignUpView.as_view(), name='signup'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/update/', AccountUpdateView.as_view(), name='update'),
    path('account/signup/guest/', GuestSignUpView.as_view(), name='guest'),

    path(
        'account/email/confirm/<key>/',
        AccountEmailActivateView.as_view(),
        name='email-activate'),
    path(
        'account/email/resend-activation/',
        AccountEmailActivateView.as_view(),
        name='resend-activation'),

    path('account/compte/<int:pk>/delete/', deleteAccount, name='delete'),
    path('account/reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('account/reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('account/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    path('account/password/change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html'),
        name='password_change'),
    path('account/password/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'),
        name='password_change_done'),
]
