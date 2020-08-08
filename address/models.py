from django.db import models
from django.urls import reverse

from payment.models import PaymentModel

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
    ('bank transfer', 'Direct bank transfer'),
)


class AddressModel(models.Model):
    payment = models.ForeignKey(
        PaymentModel, on_delete=models.CASCADE)
    full_name = models.CharField(
        'Full Name', max_length=255, blank=True)
    country = CountryField(blank_label='Choose your country')
    city = models.CharField('City', max_length=255)
    address_delivery = models.CharField(
        'Adresse delivery (optionnelle)', max_length=120, blank=True)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    postal_code = models.CharField('Code postal', max_length=255)
    phone_number = PhoneNumberField('Phone Number', null=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        return str(self.phone_number)

    def get_absolute_url(self):
        return reverse("address:address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.full_name

        return "{for_name} {phone}, {city}".format(
            for_name=for_name or "",
            phone=self.phone_number,
            city=self.city)

    def get_address(self):
        return "{for_name}\n{phone}\n{city}\n{address_delivery},\
            {address_type}\n{country}".format(
                for_name=self.full_name,
                phone=self.phone_number,
                city=self.city,
                address_delivery=self.address_delivery,
                address_type=self.address_type,
                country=self.country.name)
