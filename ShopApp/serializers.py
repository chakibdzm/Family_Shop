from rest_framework import serializers
from decimal import Decimal
from .models import *
from django.db import transaction


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'product','user', 'user_id', 'text', 'created_at')

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
'''
class ClothesSerializer(serializers.ModelSerializer):
    sub_collection_name = serializers.SerializerMethodField(method_name="get_collection_name")
    class Meta:

        model=Clothes
        fields='__all__'

    
    def get_collection_name(self, obj):
        return obj.get_collection_name()'''


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
    class Meta:
        model = Customer
        fields = ['id','user_id','phone', 'birth_date', 'membership', ]  

class FavoriteSerializer(serializers.ModelSerializer):
    prod_price=serializers.ReadOnlyField()
    prod_name=serializers.ReadOnlyField()
    prod_description=serializers.ReadOnlyField()
    prod_quantity=serializers.ReadOnlyField()
    class Meta:
        model = Favorite
        fields = ('id', 'product','prod_name','prod_price','prod_description','prod_quantity','user')








class PanierItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()
    product_name=serializers.ReadOnlyField()
    product_description=serializers.ReadOnlyField()
    product_price=serializers.ReadOnlyField()
    class Meta:
        model = PanierItem
        fields = ['product_id', 'product_name','product_description','quantity', 'product_price', 'subtotal']


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
        fields = ['id', 'user', 'items', 'created_at', 'total']
        read_only_fields = ['created_at', 'total']    

    
   
class ProductClothesChaussuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_clothes_chaussures
        fields = ('id', 'title', 'price', 'colors', 'src_image', 'alt_image', 'promotion_status', 'discount_percentage', 'quantity', 'pointure', 'description')
        