# Generated by Django 4.2.1 on 2023-05-09 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AlterField(
            model_name='proimage',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='images'),
        ),
    ]