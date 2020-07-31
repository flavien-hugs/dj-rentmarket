from django.urls import reverse
from django.contrib.sitemaps import Sitemap

from shop.models import ProductModel, CategoryModel


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['faq', 'cgu', 'contact', 'about', 'delivery']

    def location(self, item):
        return reverse(item)


class CategorySitemapView(Sitemap):
    changefreq = 'always'
    priority = 0.7

    def items(self):
        return CategoryModel.objects.all()

    def location(self, item):
        return item.get_absolute_url


class ProductSitemapView(Sitemap):
    changefreq = 'always'
    priority = 0.7

    def items(self):
        return ProductModel.objects.get_available()

    def location(self, item):
        return item.get_absolute_url
