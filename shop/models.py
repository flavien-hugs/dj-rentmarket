# import os
# import sys
# from PIL import Image
# from io import BytesIO
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils import timezone
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
# from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.sitemaps import ping_google
# from django.core.files.uploadedfile import InMemoryUploadedFile

import cloudinary
from core.utils import unique_slug_generator
from cloudinary.models import CloudinaryField

User = get_user_model()


LABEL = (('NEW', 'NEW'), ('SALE', 'SALE'), ('HOT', 'HOT'))


# def category(instance, filename):
#     f, ext = os.path.splitext(filename)
#     if ext not in ['.jpg', '.png', '.jpeg']:
#         raise NameError('Format interdit')
#     new_filename = "{}{}".format(instance.slug, ext)
#     return '/'.join(['img/category/', new_filename])


class MainCategoryModel(models.Model):
    name = models.CharField(
        'main category', max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    img = CloudinaryField('category')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'

    # def save(self):
    #     if not self.slug:
    #         self.slug = slugify(self.name)

    #     # COMPRESS THE IMAGE HERE AND THEN SAVE IT
    #     image = Image.open(self.img).convert('RGB')

    #     # RESIZE/MODIFY THE IMAGE
    #     image = image.resize((700, 700))

    #     output = BytesIO()

    #     # SAVE TO THE OUTPOUT_IO
    #     image.save(output, format='JPEG', quality=90)

    #     # change the imagefield value to be the newley modifed image value
    #     self.img = InMemoryUploadedFile(
    #         output, 'ImageField',
    #         "{}.jpg".format(self.img.name.split('.')[0]),
    #         'image/jpeg', sys.getsizeof(output), None)

    #     return super().save()

    def get_absolute_url(self):
        return reverse('shop:detail_category', kwargs={'slug': str(self.slug)})


@receiver(models.signals.pre_delete, sender=MainCategoryModel)
def delete_file(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.img.public_id)


class CategoryModel(models.Model):
    mcategory = models.ForeignKey(
        MainCategoryModel,
        on_delete=models.SET_NULL,
        blank=True, null=True)
    name = models.CharField('sub-category', max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    keywords = models.CharField(
        'keywords', max_length=200, blank=True,
        help_text='Ensemble de mots-clés SEO')

    class Meta:
        ordering = ('name',)
        verbose_name = 'sub-category'

    def __str__(self):
        return '{} ({})'.format(self.mcategory.name, self.name)

    def save(self, force_insert=False, force_update=False):
        try:
            ping_google()
        except Exception:
            pass
        return super().save()

    def get_absolute_url(self):
        return reverse('shop:detail_category', kwargs={
            'slug': str(self.slug)})

    @property
    def count_product(self):
        return ProductModel.objects.filter(
            category__name=self).count()


@receiver(models.signals.pre_save, sender=CategoryModel)
def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


# PRODUCT STRUCTURE MODEL
# def product_image_upload(instance, filename):
#     f, ext = os.path.splitext(filename)
#     if ext not in ['.jpg', '.png', '.jpeg']:
#         raise NameError('Format interdit')
#     new_filename = "{}{}".format(instance.product.slug, ext)
#     return '/'.join(['img/product/', new_filename])


class ProductModelQuerySet(models.query.QuerySet):
    def available(self):
        return self.filter(available=True)

    def featured(self):
        return self.filter(featured=True, available=True)

    def category(self):
        return self.filter(category=self.category)

    def search(self, query):
        lookups = (
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(desc__icontains=query) |
            Q(price__icontains=query) |
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


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    category = models.ManyToManyField(
        CategoryModel, verbose_name='subcategory')
    name = models.CharField('product name', max_length=200, db_index=True)
    label = models.CharField(choices=LABEL, max_length=4, blank=True)
    featured = models.BooleanField('featured', default=False)
    slug = models.SlugField(
        max_length=200, unique=True, db_index=True, blank=True)
    img = CloudinaryField('product')
    img_1 = CloudinaryField('product')
    img_2 = CloudinaryField('product')
    img_3 = CloudinaryField('product')
    img_4 = CloudinaryField('product')
    desc = models.TextField('description', blank=True)
    price = models.DecimalField('price', max_digits=10, decimal_places=2)
    available = models.BooleanField('available', default=True)
    rent_date = models.DateField('date rent', default=timezone.now)
    pub_date = models.DateField('pub date', auto_now_add=timezone.now)
    updated = models.DateField('updated', auto_now_add=timezone.now)
    views = models.PositiveIntegerField(
        'views', default=0, blank=True, editable=False)

    objects = ProductModelManager()

    class Meta:
        ordering = ('price', '-pub_date',)
        verbose_name = 'product'

    def __str__(self):
        return "%s (%s)" % (
            self.name, ", ".join(
                cat.name for cat in self.category.all()),)

    def save(self, force_insert=False, force_update=False):
        try:
            ping_google()
        except Exception:
            pass
        return super().save()

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail', kwargs={'slug': str(self.slug)})

    def get_edit_url(self):
        return reverse(
            'dashboard:product_edit', kwargs={'slug': str(self.slug)})

    def get_delete_url(self):
        return reverse(
            'dashboard:product_delete', kwargs={'slug': str(self.slug)})

    def get_update_url(self):
        return reverse(
            'dashboard:product_update', kwargs={'slug': str(self.slug)})

    @property
    def product_view_count(self, request):
        url = get_object_or_404(ProductModel, slug=self.slug)
        session_key = 'vues_{}'.format(url.pk)
        if not request.session.get(session_key, False):
            url.views += 1
            url.save()
            request.session[session_key] = True
        return 0

    # # Here I return the image
    # def get_image_url(self):
    #     img = self.productimagemodel_set.first()
    #     if not img:
    #         return '/static/img/products/product-1.jpg'
    #     return img.img.url

    # Method to create a fake table field in read only mode
    # def product_image(self):
    #     return mark_safe(
    #         '<img src="{}" width="100" height="100" />'.format(
    #             self.get_image_url()))

    # product_image.short_description = 'Image'


@receiver(models.signals.pre_save, sender=ProductModel)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class WishListModel(models.Model):
    product = models.ForeignKey(
        ProductModel, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Liste de souhait'

    def __str__(self):
        return self.wishlist


class ReviewModel(models.Model):
    product = models.ForeignKey(
        ProductModel, on_delete=models.SET_NULL, null=True)
    name = models.CharField('name', blank=True, max_length=50)
    email = models.EmailField('email', blank=True)
    comment = models.TextField('comment', blank=True)
    date = models.DateField('date', default=timezone.now)
    rating = models.CharField('rate', max_length=2, blank=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = 'review'

    def __str__(self):
        return '{} étoile(s)'.format(self.rating)

    def get_lastest_review(self):
        return ReviewModel.objects.filter(
            product__review=self).order_by('-date').first()
