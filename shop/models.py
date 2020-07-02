import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def rename(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}-{}".format(instance.slug, ext)
    return '/'.join(['img/product/', new_filename])


class CategoryModel(models.Model):

    name = models.CharField('categorie', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail_category', kwargs={'slug': str(self.slug)})


class ImageModel(models.Model):
    img1 = models.ImageField('Image_1', upload_to=rename)
    img2 = models.ImageField('Image_2', upload_to=rename, blank=True)
    img3 = models.ImageField('Image_3', upload_to=rename, blank=True)
    img4 = models.ImageField('Image_4', upload_to=rename, blank=True)
    img5 = models.ImageField('Image_5', upload_to=rename, blank=True)


# Create your models here.
class ProductModel(ImageModel):
    category = models.ManyToManyField(
        CategoryModel, verbose_name='categorie')
    name = models.CharField('Nom', max_length=200, db_index=True)
    slug = models.SlugField('Url', max_length=200, db_index=True)
    desc = models.TextField('Description', blank=True)
    price = models.DecimalField('Prix de location', max_digits=10, decimal_places=2)
    available = models.BooleanField('Disponible', default=True)
    rent_date = models.DateField('Date mise en location', default=timezone.now)
    pub_date = models.DateField('Date ajout', default=timezone.now)
    updated = models.DateField('Date mise à jour', auto_now=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

    def __str__(self):
        return "%s (%s)" % (self.name, ", ".join(
            category.name for category in self.category.all()
            ),
        )

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(ProductModel, self).save()

    def get_absolute_url(self):
        return reverse(
            'shop:produit_detail', kwargs={'slug': str(self.slug)})

    def get_view_product_count(self):
        return ProductModel.objects.filter(name=self).count()
