import os
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

from core.utils import unique_slug_generator

User = get_user_model()

LABEL = (('N', 'New'),('S', 'Sale'),)

def category(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}{}".format(instance.slug, ext)
    return '/'.join(['img/category/', new_filename])


class MainCategoryModel(models.Model):
    name = models.CharField(
        'catégorie principale', max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    img = models.ImageField('Image de description', upload_to=category)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'catégorie principale'

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save()

    def get_absolute_url(self):
        return reverse('shop:detail_category', kwargs={'slug': str(self.slug)})


class CategoryModel(models.Model):
    category = models.ForeignKey(
        MainCategoryModel, on_delete=models.CASCADE)
    name = models.CharField('sous-categorie', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    keywords = models.CharField(
        'Mots clés', max_length=200, blank=True,
        help_text='Ensemble de mots-clés SEO')

    class Meta:
        ordering = ('name',)
        verbose_name = 'catégorie'

    def __str__(self):
        return '{} ({})'.format(self.category, self.name)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(CategoryModel, self).save()

    def get_absolute_url(self):
        return reverse('shop:detail_category', kwargs={'slug': str(self.slug)})

    @property
    def count_product(self):
        return ProductModel.objects.filter(
            category__name=self).count()


# PRODUCT STRUCTURE MODEL
def product_image_upload(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}{}".format(instance.slug, ext)
    return '/'.join(['img/product/', new_filename])


class ImageModel(models.Model):
    img1 = models.ImageField(
        'Image_1', upload_to=product_image_upload, blank=True)
    img2 = models.ImageField(
        'Image_2', upload_to=product_image_upload, blank=True)
    img3 = models.ImageField(
        'Image_3', upload_to=product_image_upload, blank=True)
    img4 = models.ImageField(
        'Image_4', upload_to=product_image_upload, blank=True)
    img5 = models.ImageField(
        'Image_5', upload_to=product_image_upload, blank=True)

    class Meta:
        verbose_name = 'Image de description'

    # delet the image from file system
    def delete(self, *args, **kwargs):
        if self.img1 and self.img2 and self.img3 and self.img4 and self.img5:
            self.img1.delete()
            self.img2.delete()
            self.img3.delete()
            self.img4.delete()
            self.img5.delete()
        super().delete(*args, **kwargs)


class ProductModelQuerySet(models.query.QuerySet):
    def available(self):
        return self.filter(available=True)

    def featured(self):
        return self.filter(featured=True, available=True)

    def search(self, query):
        lookups = (
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(desc__icontains=query) |
            Q(price__icontains=query) |
            Q(keywords__icontains=query) |
            Q(label__icontains=query))

        return self.filter(lookups).distinct()


class ProductModelManager(models.Manager):
    def get_queryset(self):
        return ProductModelQuerySet(self.model, using=self._db)

    def get_available(self, *args, **kwargs):
        return self.get_queryset().available()

    def get_product_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def featured(self):
        return self.get_queryset().featured()

    def search(self, query):
        return self.get_queryset().available().search(query)

    def get_related(self, instance):
        product = self.get_queryset().filter(
            category__in=instance.category.all())
        related = (product).exclude(id=instance.id)
        return related


class ProductModel(ImageModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    category = models.ManyToManyField(
        CategoryModel, verbose_name='sous-catégorie')
    name = models.CharField('Nom', max_length=200, db_index=True)
    label = models.CharField(choices=LABEL, max_length=1, blank=True)
    featured = models.BooleanField('En vedette', default=False)
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

    objects = ProductModelManager()

    class Meta:
        ordering = ('price', '-pub_date',)
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

    def __str__(self):
        return "%s (%s)" % (
            self.name, ", ".join(
                cat.name for cat in self.category.all()),)

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

    def delete_from_location(self):
        pass


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=ProductModel)


def image_upload_to_featured(instance, filename):
    f, ext = os.path.splitext(filename)
    if ext not in ['.jpg', '.png', '.jpeg']:
        raise NameError('Format interdit')
    new_filename = "{}{}".format(instance.product.slug, ext)
    return '/'.join(['img/product/', new_filename])


class WishListModel(models.Model):
    wishlist = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Liste de souhait'

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
        return ReviewModel.objects.filter(product__review=self).order_by(
            '-date').first()
