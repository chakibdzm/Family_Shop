from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

#
class Promotion(models.Model):
    description = models.CharField(max_length=255,null=True)
    discount = models.FloatField() #poucentage 
    date_start = models.DateField()
    date_end = models.DateField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

#
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    tags = models.TextField(null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)
    

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

class Product_variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField()
    price = models.DecimalField(null=True, decimal_places=2, max_digits=100)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']


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
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    Product_variation = models.ManyToManyField(Product_variation)
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

class review(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    review_date = models.DateField(auto_now_add=True)
    comment = models.TextField(max_length=255)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    rating = models.CharField(max_length=5)  #5 stars haka

class favList(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,null=True)
    items = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    created_date = models.DateField(auto_now_add=True)

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
