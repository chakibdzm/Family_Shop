# Generated by Django 4.2.1 on 2023-06-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='points_incremented',
            field=models.BooleanField(default=False),
        ),
    ]
