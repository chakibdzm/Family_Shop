from rest_framework import serializers
from decimal import Decimal
from .models import *
from django.utils.timezone import timedelta,datetime


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'product', 'user', 'text', 'created_at')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProImage
        fields = ["id", "product", "image"]
    
    

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
    comments = CommentSerializer(many=True, read_only=True)
    

    class Meta:
        model = Product
        fields =  ['id', 'title', 'description', 'quantity', 'price','promotion_status', 'discount_percentage', 'collection_name','src_image','alt_image','taille', 'colors','comments']

    def get_collection_name(self, obj):
        return obj.get_collection_name()
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newproduct_image = ProImage.objects.create(product=product, image=image)
        return product

   
    def get_discounted_price(self, obj):
        return obj.get_discounted_price()

     

    
class ClothesSerializer(serializers.ModelSerializer):
    collection_name = serializers.SerializerMethodField(method_name="get_collection_name")
    class Meta:
        model = Clothes
        fields =  ['id', 'title', 'description','gender', 'quantity', 'price','promotion_status', 'discount_percentage', 'collection_name','src_image','alt_image','taille', 'colors','comments']


    def get_collection_name(self, obj):
        return obj.get_collection_name()

     

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            return representation

        total_amount = OrderItem.objects.filter(
            order__customer=instance,
            order__placed_at__gte= datetime.now() - timedelta(days=30)
        ).aggregate(sum('total_price'))['total_price__sum'] or 0

        if total_amount >= 50000:
            representation['membership'] = Customer.MEMBERSHIP_GOLD
        elif total_amount >= 30000:
            representation['membership'] = Customer.MEMBERSHIP_SILVER
        elif total_amount >= 10000:
            representation['membership'] = Customer.MEMBERSHIP_BRONZE

        instance.membership = representation['membership']
        instance.save()

        return representation

    class Meta:
        model = Customer
        fields = ['id','user_id','phone', 'birth_date', 'membership', ] 



class FavoriteSerializer(serializers.ModelSerializer):
    prod_price=serializers.ReadOnlyField()
    prod_name=serializers.ReadOnlyField()
    prod_description=serializers.ReadOnlyField()
    prod_quantity=serializers.ReadOnlyField()
    alt_image=serializers.ReadOnlyField()
    class Meta:
        model = Favorite
        fields = ('id', 'alt_image','product','prod_name','prod_price','prod_description','prod_quantity','user')


class PanierItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    product_name=serializers.ReadOnlyField()
    product_description=serializers.ReadOnlyField()
    product_price=serializers.ReadOnlyField()
    product_quantity=serializers.ReadOnlyField()
    alt_image=serializers.ReadOnlyField()
    class Meta:
        model = PanierItem
        fields = ['product_id', 'alt_image','product_name','product_quantity','product_description','quantity', 'product_price', 'subtotal']


    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

class AddToPanierSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)



class OrdersSerializer(serializers.ModelSerializer):
    items = PanierItemSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'user', 'items', 'address','created_at', 'total']
        read_only_fields = ['created_at', 'total']

 

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'