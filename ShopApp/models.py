from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    parent_category = models.ManyToManyField('self', symmetrical=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class Product_variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField()
    price = models.DecimalField(null=True)


class User(models.Model):
   # MEMBERSHIP_BRONZE = 'B'
    #MEMBERSHIP_SILVER = 'S'
    #MEMBERSHIP_GOLD = 'G'
    
    #MEMBERSHIP_CHOICES = [
    #    (MEMBERSHIP_BRONZE, 'Bronze'),
     #   (MEMBERSHIP_SILVER, 'Silver'),
      #  (MEMBERSHIP_GOLD, 'Gold'),
    #]
    user_name = models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    # membership = models.CharField(
    #    max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return self.user_name

    class Meta:
        ordering = ['user_name']

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(max_length=255)
    town = models.CharField()
    rue = models.CharField()
    postal_code = models.IntegerField(max_length=5)

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    Product_variation = models.ManyToManyField(Product_variation,null=True,on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

class shipping(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address,on_delete=models.CASCADE)
    shipping_method = models.CharField(max_length=255)
    shipping_cost = models.DecimalField(max_digits=10,decimal_places=2,null=True)
    shipping_date = models.DateField(auto_now_add=True)
    order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return "%s " % (self.user_name)
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4) #did not understand this
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=6, decimal_places=2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variation = models.ManyToManyField(Product_variation,null=True)
    quantity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = [['cart', 'product_variation']]

class payement(models.Model):
    order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    payment_methode = models.CharField()
    payment_date = models.DateField(auto_now_add=True)
    payment_cost = models.DecimalField(max_digits=10,decimal_places=2,null=True)

class review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    review_date = models.DateField(auto_now_add=True)
    comment = models.TextField(max_length=255)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(max_length=5)  #5 stars haka

class favList(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    items = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    created_date = models.DateField(auto_now_add=True)

class club(models.Model):
    name = models.CharField(max_length=255)
    discount_percentage = models.IntegerField()
    level = models.CharField() 
    #well hna the idea of club is not clear

class club_member(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    club = models.ForeignKey(club,on_delete=models.CASCADE)
    join_date = models.DateField()
    expiry_date = models.DateField()
    def __str__(self):
        return "%s" % (self.user.user_name)
