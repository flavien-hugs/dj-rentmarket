# Generated by Django 3.0.8 on 2020-07-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200, unique=True, verbose_name='email')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Nom')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True, verbose_name='date')),
            ],
            options={
                'verbose_name': 'Newsletter',
                'verbose_name_plural': 'Newsletters',
            },
        ),
    ]
