from decimal import Decimal
from django.conf import settings

from shop.models import ProductModel


class Location(object):

    def __init__(self, request):
        """ Initialisation du panier """
        self.session = request.session
        location = self.session.get(settings.LOCATION_SESSION_ID)
        if not location:
            location = self.session[settings.LOCATION_SESSION_ID] = {}
        self.location = location

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.location:
            self.location[product_id] = {'price': str(product.price)}
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.location:
            del self.location[product_id]
            self.save()

    def __iter__(self):
        ids_product = self.location.keys()
        products = ProductModel.objects.filter(id__in=ids_product)
        location = self.location.copy()
        for product in products:
            location[str(product.id)]['product'] = product

        for item in location.values():
            item['price'] = Decimal(item['price'])
            yield item

    # def __len__(self):
    #     return sum(item for item in self.location.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.location.values())

    def clear_session(self):
        del self.session[settings.LOCATION_SESSION_ID]
        self.save()
