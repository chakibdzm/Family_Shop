# Generated by Django 4.1.2 on 2023-03-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0006_remove_product_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=12),
            preserve_default=False,
        ),
    ]
