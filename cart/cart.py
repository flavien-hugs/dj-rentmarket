from decimal import Decimal
from django.conf import settings

from shop.models import ProductModel


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        id_product = self.cart.keys()
        products = ProductModel.objects.filter(id__in=id_product)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        id_product = str(int(product.id))
        if id_product not in self.cart:
            self.cart[id_product] = {
                'quantity': 0,
                'price': str(int(product.price))
            }

        if update_quantity:
            self.cart[id_product]['quantity'] = quantity
        else:
            self.cart[id_product]['quantity'] += quantity
        self.save()

    def save(self):
        # self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        id_product = str(int(product.id))
        if id_product in self.cart:
            del self.cart[id_product]
            self.save()

    def clear_session(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
