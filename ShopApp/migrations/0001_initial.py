# Generated by Django 4.2.1 on 2023-05-10 23:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('discount_percentage', models.IntegerField()),
                ('level', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=255)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('membership', models.CharField(choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold')], default='B', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('P', 'Pending'), ('C', 'Complete')], default='P', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ShopApp.customer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('tags', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(1)])),
                ('inventory', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='images')),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('is_archived', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, null=True)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ShopApp.product')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('K', 'Kids')], max_length=1)),
            ],
            bases=('ShopApp.product',),
        ),
        migrations.CreateModel(
            name='Sub_collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('parent_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcollections', to='ShopApp.collection')),
            ],
        ),
        migrations.CreateModel(
            name='shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_method', models.CharField(choices=[('Poste', 'Poste'), ('Yalidine', 'Yalidine')], max_length=255)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('shipping_date', models.DateField(auto_now_add=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ShopApp.order')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.address')),
            ],
        ),
        migrations.CreateModel(
            name='ProImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ShopApp.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='ShopApp.sub_collection'),
        ),
        migrations.AddField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(blank=True, to='ShopApp.promotion'),
        ),
        migrations.CreateModel(
            name='payement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_methode', models.CharField(choices=[('carte edahabia', 'carte edahabia'), ('cash on delivery', 'cash on delivery')], max_length=255)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('payment_cost', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ShopApp.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('Product', models.ManyToManyField(to='ShopApp.product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='ShopApp.order')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ShopApp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='club_member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.club')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.customer')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.customer'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ShopApp.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShopApp.product')),
            ],
            options={
                'unique_together': {('cart', 'product')},
            },
        ),
    ]
