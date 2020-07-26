import math
import random
import string
import datetime
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import Count, Sum, Avg


from shop.models import ProductModel
from address.models import AddressModel
from payment.models import PaymentModel
from location.models import LocationModel
from core.utils import unique_order_id_generator


ORDER_STATUS = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-created")

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.location_data()
        shipped = recent.not_refunded().by_status(status='shipped')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(
            updated__gte=start_date).filter(
            updated__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))

    def location_data(self):
        return self.aggregate(
            Sum("location__product__price"),
            Avg("location__product__price"),
            Count("location__product"))

    def by_status(self, status="shipped"):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status='refunded')

    def not_created(self):
        return self.exclude(status='created')

    def by_request(self, request):
        payment, created = PaymentModel.objects.new_or_get(request)
        return self.filter(payment=payment)


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, payment, location_obj):
        created = False
        qs = self.get_queryset().filter(
            payment=payment,
            location=location_obj,
            active=True,
            status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                payment=payment,
                location=location_obj)
            created = True
        return obj, created


class OrdersModel(models.Model):
    order_id = models.CharField('ID Order', max_length=255, blank=True)
    shipping_address = models.ForeignKey(
        AddressModel, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="shipping_address")
    billing_address = models.ForeignKey(
        AddressModel, on_delete=models.SET_NULL,
        related_name="billing_address", null=True, blank=True)
    shipping_address_final = models.TextField(blank=True, null=True)
    billing_address_final = models.TextField(blank=True, null=True)
    payment = models.ForeignKey(
        PaymentModel, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(
        LocationModel, on_delete=models.CASCADE, null=True, blank=True)
    shipping_total = models.DecimalField(
        default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    created = models.DateTimeField('created', auto_now_add=timezone.now)
    updated = models.DateTimeField('updated', auto_now=timezone.now)
    active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=120, default='created', choices=ORDER_STATUS)

    objects = OrderManager()

    class Meta:
        ordering = ('-updated', '-created')
        verbose_name = "Order"

    def __str__(self):
        return 'Order n° {}'.format(self.order_id)

    def save(self, *args, **kwargs):
        self.generate(10)
        super().save(*args, **kwargs)

    def generate(self, nb_carac):
        today = datetime.date.today().strftime('%d%m%y')
        carac = string.digits
        random_carac = [random.choice(carac) for _ in range(nb_carac)]
        self.order_id = today + ''.join(random_carac)

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"

    def update_total(self):
        location_total = self.location.total
        new_total = math.fsum([location_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        if self.shipping_address:
            shipping_done = True
        elif not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True

        payment = self.payment
        billing_address = self.billing_address
        total = self.total
        if payment and shipping_done and billing_address and total > 0:
            return True
        return False

    def update_purchases(self):
        for p in self.location.product.all():
            obj, created = OrderPurchaseModel.objects.get_or_create(
                order_id=self.order_id,
                product=p,
                payment=self.payment)

        return OrderPurchaseModel.objects.filter(
            order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = "paid"
                self.save()
                self.update_purchases()
        return self.status


@receiver(models.signals.pre_save, sender=OrdersModel)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = OrdersModel.objects.filter(
        location=instance.location).exclude(
        payment=instance.payment)
    if qs.exists():
        qs.update(active=False)

    if instance.shipping_address and not instance.shipping_address_final:
        instance.shipping_address_final = instance.\
            shipping_address.get_address()

    if instance.billing_address and not instance.billing_address_final:
        instance.billing_address_final = instance.billing_address.get_address()


@receiver(models.signals.post_save, sender=LocationModel)
def post_save_location_total(sender, instance, created, *args, **kwargs):
    if not created:
        location_obj = instance
        location_total = location_obj.total
        print(location_total)
        location_id = location_obj.id
        qs = OrdersModel.objects.filter(location__id=location_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


@receiver(models.signals.post_save, sender=OrdersModel)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        print("Updating... first")
        instance.update_total()


class OrderPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def by_request(self, request):
        payment, created = PaymentModel.objects.new_or_get(request)
        return self.filter(payment=payment)


class OrderPurchaseManager(models.Manager):
    def get_queryset(self):
        return OrderPurchaseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def product_by_id(self, request):
        qs = self.by_request(request)
        ids = [x.product.id for x in qs]
        return ids

    def product_by_request(self, request):
        ids = self.product_by_id(request)
        products_qs = ProductModel.objects.filter(
            id__in=ids).distinct()
        return products_qs


class OrderPurchaseModel(models.Model):
    order_id = models.CharField(max_length=120)
    payment = models.ForeignKey(
        PaymentModel, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(
        ProductModel, on_delete=models.CASCADE, blank=True)
    refunded = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OrderPurchaseManager()

    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = "Order"

    def __str__(self):
        return '{} ({})'.format(self.product.name, self.id)
