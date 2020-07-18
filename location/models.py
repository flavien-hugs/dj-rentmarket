from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, m2m_changed

from shop.models import ProductModel

User = get_user_model()


class LocationManager(models.Manager):
    def new_or_get(self, request):
        location_id = request.session.get("location_id", None)
        qs = self.get_queryset().filter(id=location_id)
        if qs.count() == 1:
            new_obj = False
            location_obj = qs.first()
            if request.user.is_authenticated and location_obj.user is None:
                location_obj.user = self.request.user
                location_obj.save()
        else:
            location_obj = LocationModel.objects.new(user=self.request.user)
            new_obj = True
            request.session['location_id'] = location_obj.id
        return location_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class LocationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    product = models.ManyToManyField(ProductModel, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = LocationManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        product = instance.product.all()
        total = 0
        for x in product:
            total += x.price
            instance.save()

m2m_changed.connect(
    m2m_changed_cart_receiver,
    sender=LocationModel.product.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = 0.00

pre_save.connect(
    pre_save_cart_receiver,
    sender=LocationModel)
