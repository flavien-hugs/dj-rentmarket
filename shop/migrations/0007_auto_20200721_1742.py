# Generated by Django 3.0.8 on 2020-07-21 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200721_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistmodel',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='wishlistmodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.ProductModel'),
        ),
        migrations.AlterField(
            model_name='reviewmodel',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.ProductModel'),
        ),
    ]
