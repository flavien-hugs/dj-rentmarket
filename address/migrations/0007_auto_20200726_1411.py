# Generated by Django 3.0.8 on 2020-07-26 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20200726_1411'),
        ('address', '0006_auto_20200726_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressmodel',
            name='payment',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentModel'),
        ),
    ]