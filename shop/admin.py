from django import forms
from django.contrib import admin

from shop.models import (
    MainCategoryModel, CategoryModel,
    ProductModel, ProductImageModel,
    ReviewModel, WishListModel)

from orders.models import OrdersModel

from analytics.models import ObjectViewedModel


admin.site.site_header = "Rent Market"
admin.site.site_title = "Rent Market Admin Portal"
admin.site.index_title = "Welcome to Rent Market Researcher Portal"

# OBJECTVIEWES ADMIN
admin.site.register(ObjectViewedModel)


class CategoryModelInline(admin.StackedInline):
    model = CategoryModel
    extra = 1

    list_display = ('mcategory', 'name', 'keywords')
    list_display_links = ('name',)
    fields = (('mcategory', 'name', 'slug'), 'keywords')
    list_per_page = 20
    ordering = ['name']
    list_filter = ['mcategory', 'name']
    search_fields = ['mcategory']
    prepopulated_fields = {'slug': ('name', 'keywords')}


# CATEGORY ADMIN
@admin.register(MainCategoryModel)
class MainCategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryModelInline]

    list_display = ('name',)
    list_filter = ['name']
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


# PRODUCT ADMIN
class ProductImageInline(admin.StackedInline):
    model = ProductImageModel
    extra = 1


# WISHLIST ADMIN
class WishListInline(admin.StackedInline):
    model = WishListModel
    extra = 1

    list_display = ('__str__', 'wishlist',)
    list_filter = ('wishlist',)


# REVIEW ADMIN
@admin.register(ReviewModel)
class ReviewModelInline(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_per_page = 20
    fields = (('product', 'name', 'email'), ('rating', 'date'), 'comment')
    search_fields = ['product']
    list_display_links = ('product',)
    list_display = (
        '__str__', 'product', 'name', 'email',
        'comment', 'date', 'rating',)
    list_filter = ['date', 'rating']


# PRODUCT ADMIN
@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, WishListInline]

    date_hierarchy = 'updated'
    list_display = (
        'user', 'name', 'price',
        'available', 'featured',
        'rent_date', 'pub_date')
    list_display_links = ('name',)

    fields = (
        'user',
        'category',
        ('name', 'slug'),
        ('label', 'price'), 'rent_date',
        ('available', 'featured'),
        'desc',
    )
    list_filter = [
        'available', 'category',
        'label', 'rent_date', 'pub_date']
    list_editable = ['price', 'available']
    search_fields = ['name', 'price']
    prepopulated_fields = {
        'slug': ('name', 'price', 'label')
    }

    def clean_date(self):
        if self.cleaned_data['rent_date'] <= self.cleaned_data['pub_date']:
            raise forms.ValidationError(
                'Rent Date not inferieur for Pub date.')
        return self.cleaned_data['rent_date']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.save()
        for afile in request.FILES.getlist('photos_multiple'):
            obj.productimagemodels.create(img=afile)

admin.site.register(OrdersModel)
