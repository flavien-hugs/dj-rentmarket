from django.db import models
from django.db.models import Q
from datetime import timedelta
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


from core.utils import unique_key_generator
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

DEFAULT_ACTIVATION_DAYS = getattr(
    settings, 'DEFAULT_ACTIVATION_DAYS', 7)


# MODEL MANAGER
class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email or not password:
            raise ValueError(
                "Email ou mot de passe incorrecte")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name)

        user.set_password(password)

        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True)
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_admin=True,
            is_staff=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Adresse email', unique=True, max_length=255)
    full_name = models.CharField(
        'Nom & prénoms', max_length=225, blank=True, null=True)
    country = CountryField()
    city = models.CharField('Ville', max_length=50)
    phone_number = PhoneNumberField('Téléphone', null=True)
    joined = models.DateField('joined date', auto_now_add=timezone.now)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff


class EmailActivationQuerySet(models.query.QuerySet):
    def confirmed(self):
        now = timezone.now()
        sr = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        er = now
        return self.filter(
            activated=False,
            forced_expired=False).filter(
            created__gt=sr, created__lte=er)


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(
            self.model, using=self._db)

    def confirmed(self):
        return self.get_queryset().confirmed()

    def email_exists(self, email):
        return self.get_queryset().filter(
            Q(email=email) | Q(user__email=email)
            ).filter(activated=False)


class EmailActivationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expired = models.IntegerField(default=7)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("shop:vendor_detail", kwargs={
            "username": self.email})

    def can_activate(self):
        queryset = EmailActivationModel.objects.filter(
            pk=self.pk).confirmed()
        if queryset.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def re_generate_token(self):
        self.key = None
        self.save()
        if self.key is not None:
            print(self.key)
            return True
        return False

    def send_token_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(
                    settings,
                    'BASE_URL', 'https://unsta.pythonanywhere.com')
                key_path = reverse(
                    'accounts:email-activate',
                    kwargs={'key': self.key})
                path = '{base}{path}'.format(
                    base=base_url,
                    path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }

                txt = get_template(
                    'accounts/verify/verify.txt').render(context)
                html = get_template(
                    'accounts/verify/verify.html').render(context)
                subject = 'Click email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                    subject, txt, from_email, recipient_list,
                    html_message=html, fail_silently=False,)
                return sent_mail
        return False


@receiver(models.signals.pre_save, sender=EmailActivationModel)
def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


@receiver(models.signals.post_save, sender=User)
def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivationModel.objects.create(
            user=instance, email=instance.email)
        obj.send_token_activation()


class GuestEmailModel(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
