# Generated by Django 4.1.7 on 2023-03-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0009_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
    ]
