# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import CategoryModel, ProductModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    """ Admin View for CategorieAdmin """
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    """ Admin View for ProduitAdmin """
    model = ProductModel
    date_hierarchy = 'updated'
    list_display = ('name', 'price', 'available', 'rent_date', 'pub_date')
    list_display_links = ('name',)
    list_filter = ['available', 'rent_date', 'pub_date']
    list_editable = ['price', 'available']
    search_fields = ['name', 'price']
    prepopulated_fields = {'slug': ('name',)}

    def clean_date(self):
        if self.cleaned_data['rent_date'] <= self.cleaned_data['pub_date']:
            raise forms.ValidationError('Rent Date not inferieur for Pub date.')
        return self.cleaned_data['rent_date']
