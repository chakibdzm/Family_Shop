# Generated by Django 4.2.1 on 2023-06-02 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='membership',
            field=models.CharField(blank=True, choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold')], default=None, max_length=1),
        ),
    ]
