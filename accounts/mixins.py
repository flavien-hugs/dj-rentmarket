import datetime
from django.db.models import Sum, Avg
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


from payment.models import PaymentModel
from shop.models import ProductModel

# GETTING MY MODEL USER
User = get_user_model()


class UserAccountMixin(LoginRequiredMixin, object):
    account = None
    product = []

    def get_account(self):
        account = User.objects.filter(full_name=self.request.user)
        if account.exists() and account.count() == 1:
            self.account = account.first()
            return account.first()
        return None

    def get_product(self):
        product = ProductModel.objects.get_available(
            ).filter(user=self.get_account())
        self.product = product
        print(product)
        return product

    def get_payment(self):
        payment = PaymentModel.objects.filter(
            product__in=self.get_product())
        print(payment)
        return payment

    def get_payment_today(self):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        return self.get_payment().filter(
            created__range=(today_min, today_max))

    def get_total_sale(self):
        payment = self.get_payment().aggregate(Sum("price"))
        total_sale = payment["price__sum"]
        print(total_sale)
        return total_sale

    def get_today_sale(self):
        payment = self.get_payment_today(
            ).aggregate(Sum("price"), Avg("price"))
        total_sale = payment["price__sum"]
        print(total_sale)
        return total_sale
