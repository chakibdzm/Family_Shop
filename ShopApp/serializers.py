from rest_framework import serializers
from decimal import Decimal
from .models import *
#from .models import Favorite
from django.db import transaction


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']
    
    

class SubCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sub_collection
        fields=['id','parent_collection','title']
    products_count = serializers.IntegerField(read_only=True)

class ClothesSerializer(serializers.ModelSerializer):
    sub_collection_name = serializers.SerializerMethodField(method_name="get_collection_name")
    class Meta:

        model=Clothes
        fields=['id', 'title','gender', 'description', 'slug', 'inventory', 'unit_price','discounted_price', 'price_with_tax', 'sub_collection_name','tags']

    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    discounted_price = serializers.SerializerMethodField(method_name='get_discounted_price')
    def get_collection_name(self, obj):
        return obj.get_collection_name()
    
    def get_discounted_price(self, obj):
        return obj.get_discounted_price()

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
##
class ProductSerializer(serializers.ModelSerializer):
    collection_name = serializers.SerializerMethodField(method_name="get_collection_name")

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price','discounted_price', 'price_with_tax', 'collection_name','tags']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    discounted_price = serializers.SerializerMethodField(method_name='get_discounted_price')
    def get_collection_name(self, obj):
        return obj.get_collection_name()

    #collection = serializers.HyperlinkedRelatedField(
    #    queryset = Collection.objects.all(),
    #    view_name='collection-detail'
    #)

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']    
      

class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
    total_price = serializers.SerializerMethodField(method_name='calculate_price') 

    def calculate_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
    total_price = serializers.SerializerMethodField(method_name='calculate_total')   

    def calculate_total(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()]) 


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']        


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance    

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user','items','status', 'placed_at']

class AddOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            (customer, created) = Customer.objects.get_or_create(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    price = item.product.unit_price,
                    quantity = item.quantity
                )for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete
            return order

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone', 'birth_date', 'membership', ]  

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'product', 'created_at')

    
    #permission_classes = (permissions.IsAuthenticated,)

#class FavListSerializer(serializers.ModelSerializer):
   # product_id = serializers.IntegerField()
   # user_id = serializers.IntegerField(read_only=True)
   # class Meta:
    #    model = favList
     #   fields = ['id','product_id','user_id','created_at']

#class AddFavSerializer(serializers.ModelSerializer):
 #   product_id = serializers.IntegerField()
#
 #   def validate_product_id(self, value):
  #      if not Product.objects.filter(pk=value).exists():
   #         raise serializers.ValidationError('No product with the given ID was found.')
    #    return value
    #def save(self, **kwargs):
     #   fav_id = self.context['fav_id']
      #  product_id = self.validated_data['product_id']
       # try:
        #    favItem = favList.objects.get(product_id= product_id,fav_id=fav_id)
         #   self.instance = serializers.ValidationError('This product is already in your favorites.')
        #except favItem.DoesNotExist:
        #    favItem = favList.objects.create(fav_id=fav_id, product_id=product_id)
         #   favItem.save()
         #   self.instance = favItem
        #return self.instance

   # class Meta:
    #    model = favList
     #   fields = ['id','product_id']

#class ReviewSerializer(serializers.ModelSerializer):
   # user_id = serializers.IntegerField(read_only=True)
   # product_id =serializers.IntegerField()
   # class Meta:
    #    model = review
     #   fields = ['id','product_id','user_id','rating','comment','crated_at','updated_at']

