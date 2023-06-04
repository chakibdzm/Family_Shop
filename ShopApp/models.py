from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from django.contrib import admin
from django.utils import timezone

#from datetime import timedelta
class ProductAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    
    def archive_selected_products(modeladmin, request, queryset):
        queryset.update(is_archived=True)
    archive_selected_products.short_description = "Archive selected products"
    actions = [archive_selected_products]
    list_display = ['title', 'is_archived']



class Promotion(models.Model):
    description = models.CharField(max_length=255,null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2) #poucentage 
    date_start = models.DateField()
    date_end = models.DateField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

class Sub_collection(models.Model):
    title=models.CharField(max_length=255)
    parent_collection=models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='subcollections')
      
    def __str__(self) ->str:
        return self.title
#
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    promotion_status = models.SmallIntegerField()
    discount_percentage = models.IntegerField()
    src_image = models.CharField(max_length=255)
    alt_image = models.CharField(max_length=255)
    collection = models.ForeignKey(Sub_collection, on_delete=models.CASCADE, related_name='products', null=True)
    is_archived = models.BooleanField(default=False)
    taille = models.CharField(max_length=255)
    colors = models.CharField(max_length=255)

    def __str__(self):
        return (self.title)
    def get_collection_name(self):
        return self.collection.title
    

class ProImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "images")
    image = models.ImageField(upload_to="images", default="", null=True, blank=True)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-created_at']

class Clothes(Product):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('K', 'Kids'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def get_collection_name(self):
        return self.collection.title
    
    class Meta:
        db_table = 'ShopApp_clothes'


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #def is_deletable(self):
    #    """Returns True if the order can be deleted by the user."""
    #    now = timezone.now()
    #    return self.placed_at + timedelta(days=3) > now

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,related_name='items')
    Product = models.ManyToManyField(Product)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)

class shipping(models.Model):
    shipping_methodes = [
        ('Poste', 'Poste'),
        ('Yalidine', 'Yalidine')
    ]
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    shipping_method = models.CharField(choices=shipping_methodes, max_length=255)
    shipping_cost = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    shipping_date = models.DateField(auto_now_add=True)
    order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return "%s " % (self.user_name)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )


    class Meta:
        unique_together = [['cart', 'product']]

class payement(models.Model):
    payment_methodes = [
        ('carte edahabia', 'carte edahabia'),
        ('cash on delivery', 'cash on delivery')
    ]
    order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    payment_methode = models.CharField(choices=payment_methodes, max_length=255)
    payment_date = models.DateField(auto_now_add=True)
    payment_cost = models.DecimalField(max_digits=10,decimal_places=2,null=True)



class club(models.Model):
    name = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()
    level = models.CharField(max_length=255) 
    #well hna the idea of club is not clear

class club_member(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE)
    club = models.ForeignKey(club,on_delete=models.CASCADE)
    join_date = models.DateField()
    expiry_date = models.DateField()
    def __str__(self):
        return "%s" % (self.user.user_name)
    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='fav_product')
    
    class Meta:
        unique_together = ('user', 'product')

    def prod_name(self):
        return self.product.title
    def prod_price(self):
        return self.product.price
    def prod_description(self):
        return self.product.description
    def prod_quantity(self):
        return self.product.quantity

class PanierItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)


    def subtotal(self):
        return self.quantity * self.price
    
    def product_name(self):
        return self.product.title
    
    def product_description(self):
        return self.product.description
    
    def product_price(self):
        return self.price

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'
    
    



class Orders(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('PanierItem')
    created_at = models.DateTimeField(default=timezone.now)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())    

    def __str__(self) -> str:
        return str(self.user) 
    
    def get_items_by_product_name(self,product_name):
        return self.items.filter(product__product__title=product_name)
    

    
    
    

class product_clothes_chaussures(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    colors = models.CharField(max_length=255)
    src_image = models.CharField(max_length=255)
    alt_image = models.CharField(max_length=255)
    promotion_status = models.SmallIntegerField()
    discount_percentage = models.IntegerField()
    quantity = models.IntegerField()
    pointure = models.CharField(max_length=255)
    description = models.TextField() 


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message