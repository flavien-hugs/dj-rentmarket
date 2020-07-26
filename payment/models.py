import os
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth import get_user_model

import stripe
from accounts.models import GuestEmailModel


STRIPE_SECRET_KEY = os.environ.get(
    "STRIPE_SECRET_KEY",
    "sk_test_51H6F3bEVRs2R6z6LBLDgt4mlR50t4QHqDGb1BJ1A7NII7ejhXPVMlA9tnlWMy8WWtPjrQrtXeHBRcsfXdJwjmQL700iWChY2Zj")

stripe.api_key = STRIPE_SECRET_KEY

User = get_user_model()


class PaymentManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmailModel.objects.get(
                id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj, created


class PaymentModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = PaymentManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return ChargeModel.objects.do(self, order_obj, card)

    def get_card(self):
        return self.cardmodel_set.all()

    def get_payment_method_url(self):
        return reverse('payment:method')

    @property
    def has_card(self):
        return self.get_card().exists()

    @property
    def default_card(self):
        d_card = self.get_card().filter(active=True, default=True)
        if d_card.exists():
            return d_card.first()
        return None

    def set_card_inactive(self):
        card_qs = self.get_card()
        card_qs.update(active=False)
        return card_qs.filter(active=True).count()


@receiver(models.signals.pre_save, sender=PaymentModel)
def payment_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = stripe.Customer.create(email=instance.email)
        print(customer)
        instance.customer_id = customer.id


@receiver(models.signals.post_save, sender=User)
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        PaymentModel.objects.get_or_create(user=instance, email=instance.email)


class CardManager(models.Manager):

    def all(self, *args, **kwargs):
        return self.get_queryset().filter(active=True)

    def add_new(self, payment, token):
        if token:
            customer = stripe.Customer.retrieve(payment.customer_id)
            stripe_card_response = customer.sources.create(source=token)
            new_card = self.model(
                payment=payment,
                stripe_id=stripe_card_response.id,
                brand=stripe_card_response.brand,
                country=stripe_card_response.country,
                exp_month=stripe_card_response.exp_month,
                exp_year=stripe_card_response.exp_year,
                last4=stripe_card_response.last4)

            new_card.save()
            return new_card
        return None


class CardModel(models.Model):
    payment = models.ForeignKey(
        PaymentModel, on_delete=models.CASCADE, blank=True)
    stripe_id = models.CharField(max_length=120)
    brand = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)


@receiver(models.signals.post_save, sender=CardModel)
def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        payment = instance.payment
        qs = CardModel.objects.filter(
            payment=payment).exclude(pk=instance.pk)
        qs.update(default=False)


class ChargeManager(models.Manager):
    def do(self, payment, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            card = payment.cardmodel_set.filter(default=True)
            if card.exists():
                card_obj = card.first()
        if card_obj is None:
            return False, "No card available"
        c = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency="usd",
            customer=payment.customer_id,
            source=card_obj.stripe_id,
            metadata={"order_id": order_obj.order_id},)
        new_charge_obj = self.model(
            payment=payment,
            stripe_id=c.id,
            paid=c.paid,
            refunded=c.refunded,
            outcome=c.outcome,
            outcome_type=c.outcome['type'],
            seller_message=c.outcome.get('seller_message'),
            risk_level=c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class ChargeModel(models.Model):
    payment = models.ForeignKey(PaymentModel, on_delete=models.CASCADE, blank=True)
    stripe_id = models.CharField(max_length=120)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()
