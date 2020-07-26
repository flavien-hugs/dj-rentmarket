# Generated by Django 3.0.8 on 2020-07-26 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_auto_20200726_1353'),
        ('orders', '0004_auto_20200726_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersmodel',
            name='shipping_address',
            field=models.ForeignKey(blank=True, default=12, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='address.AddressModel'),
            preserve_default=False,
        ),
    ]
