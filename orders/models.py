from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

from shop.models import ProductModel

from django_countries.fields import CountryField


class OrdersModel(models.Model):
    first_name = models.CharField('Nom', max_length=50)
    last_name = models.CharField('Prénoms', max_length=50)
    company = models.CharField('Entreprise (optionnel)', max_length=50, blank=True)
    country = CountryField(blank_label='selectionner votre pays')
    address = models.CharField('Adresse de livraison', max_length=50)
    apartement = models.CharField('Appartement (optionnel)', max_length=30, blank=True)
    city = models.CharField('Ville', max_length=50)
    zipcode = models.CharField('Code postal / ZIP', max_length=10)
    email = models.EmailField('Adresse Email')
    phone = models.CharField('Téléphone', max_length=10)
    note = models.TextField('Note de commande (optionnelle)', blank=True)
    created = models.DateTimeField('Créé', auto_now_add=True)
    updated = models.DateTimeField('Mise à jour', auto_now=True)
    louer = models.BooleanField('Louer', default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return 'Commande_{}'.format(self.id)


class ItemOrderModel(models.Model):
    order = models.ForeignKey(OrdersModel, related_name='commande',
        on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, related_name='produit',
        on_delete=models.CASCADE)
    price = models.DecimalField('Prix', max_digits=10, decimal_places=2)
    date = models.DateField('Date Commande', auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('-date',)
        verbose_name = "Objet Commandé"
        verbose_name_plural = "Objets Commandés"

    def __str__(self):
        return str(self.order.id)

    def get_depense(self):
        return self.price
