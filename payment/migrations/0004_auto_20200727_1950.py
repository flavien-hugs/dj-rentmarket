# Generated by Django 3.0.8 on 2020-07-27 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0003_auto_20200726_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardmodel',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentModel'),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentModel'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]