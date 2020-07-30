# Generated by Django 3.0.8 on 2020-07-30 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
        ('location', '0001_initial'),
        ('shop', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=255, verbose_name='ID Order')),
                ('shipping_address_final', models.TextField(blank=True, null=True)),
                ('billing_address_final', models.TextField(blank=True, null=True)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=5.99, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded')], default='created', max_length=120)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='address.AddressModel')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.LocationModel')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentModel')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='address.AddressModel')),
            ],
            options={
                'verbose_name': 'Order',
                'ordering': ('-updated', '-created'),
            },
        ),
        migrations.CreateModel(
            name='OrderPurchaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=120)),
                ('refunded', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentModel')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.ProductModel')),
            ],
            options={
                'verbose_name': 'Order',
                'ordering': ['-created', '-updated'],
            },
        ),
    ]
