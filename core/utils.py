import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, carac=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(carac) for _ in range(size))


def unique_key_generator(instance):
    size = random.randint(20, 45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qsx = Klass.objects.filter(
        key=key).exists()
    if qsx:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4))
        return unique_slug_generator(
            instance, new_slug=new_slug)
    return slug
