# Generated by Django 4.1.2 on 2023-03-22 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0005_product_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
    ]
