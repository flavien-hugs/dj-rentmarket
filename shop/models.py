import os
from django.db import models
from django.urls import reverse
from django.utils import timezone


def rename(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}-{}".format(instance.slug, ext)
    return '/'.join(['img/product/', new_filename])


class Category(models.Model):

    name = models.CharField('categorie', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='categorie',
        on_delete=models.CASCADE)
    name = models.CharField('Nom', max_length=200, db_index=True)
    slug = models.SlugField('Url', max_length=200, db_index=True)
    description = models.TextField('Description', blank=True)
    price = models.DecimalField('Prix', max_digits=10, decimal_places=2)
    available = models.BooleanField('Disponible', default=True)
    created = models.DateField('Date ajout', default=timezone.now)
    updated = models.DateField('Date mise à jour', auto_now=True)
    img1 = models.ImageField('IMG1', upload_to=rename, blank=True)
    img2 = models.ImageField('IMG2', upload_to=rename, blank=True)
    img3 = models.ImageField('IMG3', upload_to=rename)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse(
    #         'shop:produit_detail', kwargs={'slug': str(self.slug)})
