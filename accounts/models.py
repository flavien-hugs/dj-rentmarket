from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


# MODEL MANAGER
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError('user must provide an email')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)

        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password, is_staff=True, is_active=True)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email, password=password,
            is_admin=True, is_staff=True, is_active=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Adresse email', unique=True, max_length=255)
    first_name = models.CharField('Prénoms', max_length=50)
    last_name = models.CharField('Nom', max_length=50)
    country = CountryField()
    city = models.CharField('Ville', max_length=50)
    phone_number = PhoneNumberField('Téléphone', null=True)
    joined = models.DateField('date joined', auto_now_add=timezone.now)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name.upper())

    def get_short_name(self):
        return self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff
