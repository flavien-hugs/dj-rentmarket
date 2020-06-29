from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView,
    PasswordChangeDoneView)
from accounts.views import signup, AccountUpdateView

app_name = 'accounts'
urlpatterns = [
    path('acount/signup/', signup, name='signup'),
    path('acount/login/', LoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('acount/logout/', LogoutView.as_view(), name='logout'),
    path('acount/ompte/', AccountUpdateView.as_view(), name='updated'),
    path('customer/account/reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('customer/account/reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    path('customer/account/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('customer/account/reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    path('customer/account/password/change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html'),
        name='password_change'),
    path('customer/account/password/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'),
        name='password_change_done'),
]
