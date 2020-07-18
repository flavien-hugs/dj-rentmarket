from django.contrib import admin

from shop.models import (
    MainCategoryModel, CategoryModel,
    ProductModel, ReviewModel, WishListModel)
from orders.models import OrdersModel

from analytics.models import ObjectViewedModel


admin.site.site_header = "Rent Market"
admin.site.site_title = "Rent Market Admin Portal"
admin.site.index_title = "Welcome to Rent Market Researcher Portal"


admin.site.register(ObjectViewedModel)


@admin.register(WishListModel)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'wishlist',)
    list_filter = ('wishlist',)


@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_per_page = 20
    search_fields = ['product']
    list_display_links = ('product',)
    list_display = (
        'id', 'product', 'name', 'email', 'comment', 'date', 'rating',)


@admin.register(MainCategoryModel)
class MainCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category', 'name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    model = ProductModel
    date_hierarchy = 'updated'
    list_display = ('user', 'name', 'price', 'available', 'featured', 'rent_date', 'pub_date')
    list_display_links = ('name',)
    list_filter = ['available', 'label', 'rent_date', 'pub_date', 'keywords']
    list_editable = ['price', 'available']
    search_fields = ['name', 'price']
    prepopulated_fields = {'slug': ('name',)}

    def clean_date(self):
        if self.cleaned_data['rent_date'] <= self.cleaned_data['pub_date']:
            raise forms.ValidationError('Rent Date not inferieur for Pub date.')
        return self.cleaned_data['rent_date']

admin.site.register(OrdersModel)
