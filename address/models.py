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
    first_name = models.CharField(
        'Nom', max_length=255, null=True, blank=True,
        help_text='Shipping to? Who is it for?')
    last_name = models.CharField(
        'Prénoms', max_length=255, null=True, blank=True)
    country = CountryField(blank_label='selectionner votre pays')
    city = models.CharField('Ville', max_length=255)
    address_delivery = models.CharField('Adresse de livraison', max_length=120)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    zipcode = models.CharField('Code postal/ZIP', max_length=255)
    phone_number = PhoneNumberField('Téléphone', null=True)
    note = models.TextField('Note de commande (optionnelle)', blank=True)

    def __str__(self):
        if self.first_name:
            return str(self.first_name)
        return str(self.phone_number)

    def get_absolute_url(self):
        return reverse("address:update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.first_name

        if self.last_name:
            for_name = "{} | {},".format(
                self.last_name, for_name)
        return "{for_name} {line1}, {city}".format(
            for_name=for_name or "",
            line1=self.phone_number,
            city=self.city)

    def get_address(self):
        return "{for_name}\n{line1}\n{city}\n{address_delivery},\
            {address_type}\n{country}".format(
                for_name=self.first_name or "",
                line1=self.phone_number,
                city=self.city,
                address_delivery=self.address_delivery,
                address_type=self.address_type,
                country=self.country.name)
