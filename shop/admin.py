from django.contrib import admin

from shop.models import Category, Product


# Register your models here.
admin.site.site_header = "RentMarket Admin"
admin.site.site_title = "RentMarketAdmin Portal"
admin.site.index_title = "RentMarket Researcher Portal"

admin.site.register(Category)
admin.site.register(Product)
