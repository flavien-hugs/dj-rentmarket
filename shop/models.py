import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


def product(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}{}".format(instance.slug, ext)
    return '/'.join(['img/product/', new_filename])


def category(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}{}".format(instance.slug, ext)
    return '/'.join(['img/category/', new_filename])


class MainCategoryModel(models.Model):
    name = models.CharField(
        'catégorie principale', max_length=200, unique=True, default=1)
    slug = models.SlugField(max_length=200, unique=True)
    img = models.ImageField('Image de description', upload_to=category)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'catégorie principale'
        verbose_name_plural = 'catégories principales'

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(MainCategoryModel, self).save()


class CategoryModel(models.Model):
    category = models.ForeignKey(
        MainCategoryModel, verbose_name='catégorie principale',
        on_delete=models.CASCADE)
    name = models.CharField('sous-categorie', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    keywords = models.CharField(
        'Mots clés', max_length=200, blank=True,
        help_text='Ensemble de mots-clés SEO')

    class Meta:
        ordering = ('name',)
        verbose_name = 'catégorie'
        verbose_name_plural = 'catégories'

    def __str__(self):
        return '{} ({})'.format(self.category, self.name)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(CategoryModel, self).save()

    def get_absolute_url(self):
        return reverse('shop:detail_category', kwargs={'slug': str(self.slug)})


class ImageModel(models.Model):
    img1 = models.ImageField('Image_1', upload_to=product, blank=True)
    img2 = models.ImageField('Image_2', upload_to=product, blank=True)
    img3 = models.ImageField('Image_3', upload_to=product, blank=True)
    img4 = models.ImageField('Image_4', upload_to=product, blank=True)
    img5 = models.ImageField('Image_5', upload_to=product, blank=True)

    class Meta:
        verbose_name = 'Image de description'


# Create your models here.
class ProductModel(ImageModel):
    LABEL = (('N', 'New'),('S', 'Sale'),)

    user = models.ForeignKey(
        User, related_name='utilisateur', on_delete=models.CASCADE, blank=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE,
        verbose_name='sous-catégorie')
    name = models.CharField('Nom', max_length=200, db_index=True)
    label = models.CharField(choices=LABEL, max_length=1, blank=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    desc = models.TextField('Description', blank=True)
    price = models.DecimalField(
        'Prix de location', max_digits=10, decimal_places=2)
    available = models.BooleanField('Disponible', default=True)
    rent_date = models.DateField('Date mise en location', default=timezone.now)
    keywords = models.CharField(
        'Mot clés', max_length=255, help_text='Ensemble de mots-clés SEO')
    pub_date = models.DateField('Date ajout', auto_now_add=timezone.now)
    updated = models.DateField('Date mise à jour', auto_now_add=timezone.now)
    views = models.PositiveIntegerField('Nombre de vues', default=0)

    class Meta:
        ordering = ('price', '-pub_date',)
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

    def __str__(self):
        return "{} ({})".format(self.name, self.category)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(ProductModel, self).save()

    def get_absolute_url(self):
        return reverse(
            'shop:produit_detail', kwargs={'slug': str(self.slug)})

    def get_edit_url(self):
        return reverse(
            'dashboard:product_edit', kwargs={'slug': str(self.slug)})

    def get_delete_url(self):
        return reverse(
            'dashboard:product_delete', kwargs={'pk': str(self.id)})

    def get_update_url(self):
        return reverse(
            'dashboard:product_update', kwargs={'slug': str(self.slug)})


class WishListModel(models.Model):
    wishlist = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Liste de souhaits'

    def __str__(self):
        return self.wishlist


class ReviewModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    name = models.CharField('Nom', max_length=50)
    email = models.EmailField('adresse email')
    comment = models.TextField('Votre commentaire sur le produit')
    date = models.DateField('Date', default=timezone.now)
    rating = models.CharField('notes', max_length=2, blank=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return '{} étoile(s)'.format(self.rating)

    def get_lastest_review(self):
        return ReviewModel.objects.filter(
            product__review=self).order_by(
            '-date').first()
