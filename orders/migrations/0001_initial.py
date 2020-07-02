# Generated by Django 3.0.7 on 2020-07-02 13:16

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('last_name', models.CharField(max_length=50, verbose_name='Prénoms')),
                ('company', models.CharField(blank=True, max_length=50, verbose_name='Entreprise (optionnel)')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('address', models.CharField(max_length=50, verbose_name='Adresse de livraison')),
                ('apartement', models.CharField(blank=True, max_length=30, verbose_name='Appartement (optionnel)')),
                ('city', models.CharField(max_length=50, verbose_name='Ville')),
                ('zipcode', models.CharField(max_length=10, verbose_name='Code postal / ZIP')),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse Email')),
                ('phone', models.CharField(max_length=10, verbose_name='Téléphone')),
                ('note', models.TextField(blank=True, verbose_name='Note de commande (optionnelle)')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Créé')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Mise à jour')),
                ('louer', models.BooleanField(default=False, verbose_name='Louer')),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ItemOrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Prix')),
                ('date', models.DateField(auto_now=True, verbose_name='Date Commande')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commande', to='orders.OrdersModel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produit', to='shop.ProductModel')),
            ],
            options={
                'verbose_name': 'Objet Commandé',
                'verbose_name_plural': 'Objets Commandés',
                'ordering': ('-date',),
            },
        ),
    ]