from django.contrib import admin

from shop.models import ProductModel, CategoryModel


# Register your models here.
admin.site.site_header = "RentMarket Admin"
admin.site.site_title = "RentMarketAdmin Portal"
admin.site.index_title = "RentMarket Researcher Portal"

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
