import random
import string
import datetime
from django.db import models
from django.utils import timezone

from shop.models import ProductModel
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class OrdersModel(models.Model):
    order_id = models.CharField(
        'ID commande', max_length=255, blank=True)
    first_name = models.CharField('Nom', max_length=255)
    last_name = models.CharField('Prénoms', max_length=255)
    company = models.CharField(
        'Entreprise (optionnel)', max_length=255, blank=True)
    country = CountryField(blank_label='selectionner votre pays')
    address = models.CharField('Adresse de livraison', max_length=50)
    apartement = models.CharField(
        'Appartement (optionnel)', max_length=255, blank=True)
    city = models.CharField('Ville', max_length=255)
    zipcode = models.CharField('Code postal/ZIP', max_length=255)
    email = models.EmailField('Adresse Email')
    phone_number = PhoneNumberField('Téléphone', null=True)
    note = models.TextField('Note de commande (optionnelle)', blank=True)
    created = models.DateTimeField('Créé', auto_now_add=timezone.now)
    updated = models.DateTimeField('Mise à jour', auto_now_add=timezone.now)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return 'Commande n° {}'.format(self.order_id)

    def save(self, *args, **kwargs):
        self.generate(10)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%y%m%d')
        carac = string.digits + string.ascii_uppercase
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.order_id = today + ''.join(random_carac)


class ItemOrderModel(models.Model):
    order = models.ForeignKey(
        OrdersModel, related_name='commande', on_delete=models.CASCADE)
    product = models.ForeignKey(
        ProductModel, related_name='product', on_delete=models.CASCADE)
    price = models.DecimalField('Prix', max_digits=10, decimal_places=2)
    date = models.DateField('Date Commande', auto_now_add=timezone.now)

    class Meta:
        ordering = ('-date',)
        verbose_name = "Objet Commandé"
        verbose_name_plural = "Objets Commandés"

    def __str__(self):
        return str(self.id)

    def get_depense(self):
        return self.price
