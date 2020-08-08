# RECOMMENDER SYSTEM

import redis
from django.conf import settings
from shop.models import ProductModel


# START REDIS SERVER
r = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )


class Recommender(object):

    def get_product_id(self, id):
        return 'product:{}:purchased_witgh'.format(id)

    def product_bought(self, products):
        product_ids = [obj.id for obj in products]

        for product_id in product_ids:
            print(product_id)
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_id(
                        str[product_id]), with_id, amount=1)

    def suggest_products(self, products, max=50):
        product_ids = [obj.id for obj in products]
        if len(products) == 1:
            suggests = r.zrange(
                self.get_product_id(product_ids[0]),
                0, -1, desc=True)[:max]
        else:
            flat_ids = ''.join([str(id) for id in product_ids])
            temp_key = 'temp_{}'.format(flat_ids)
            keys = [self.get_produit_id(id) for id in product_ids]
            r.zunionstore(temp_key, keys)
            r.zrem(temp_key, *product_ids)
            suggests = r.zrange(temp_key, 0, -1, desc=True)[:max]
            r.delete(temp_key)

        suggested_products_ids = [int(id) for id in suggests]
        suggested_products = list(
            ProductModel.objects.filter(
                id__in=suggested_products_ids))
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products

    def clear_purchases(self):
        for id in ProductModel.objects.values_list('id', flat=True):
            r.delete(self.get_produit_id(id))
