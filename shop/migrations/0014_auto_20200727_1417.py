# Generated by Django 3.0.8 on 2020-07-27 14:17

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20200726_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimagemodel',
            name='img',
            field=models.FileField(blank=True, upload_to=shop.models.product_image_upload),
        ),
    ]