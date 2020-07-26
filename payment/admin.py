from django.contrib import admin

from payment.models import PaymentModel, CardModel, ChargeModel

admin.site.register(PaymentModel)
admin.site.register(CardModel)
admin.site.register(ChargeModel)
