# Generated by Django 3.0.8 on 2020-07-12 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_ordersmodel_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersmodel',
            name='order_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='ID commande'),
        ),
        migrations.AlterField(
            model_name='ordersmodel',
            name='address',
            field=models.CharField(max_length=50, verbose_name='Adresse de livraison'),
        ),
    ]
