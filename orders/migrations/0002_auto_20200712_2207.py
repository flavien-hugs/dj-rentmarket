# Generated by Django 3.0.8 on 2020-07-12 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordersmodel',
            name='louer',
        ),
        migrations.AlterField(
            model_name='ordersmodel',
            name='zipcode',
            field=models.CharField(max_length=10, verbose_name='Code postal/ZIP'),
        ),
    ]
