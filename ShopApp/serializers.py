from rest_framework import serializers
from decimal import Decimal
from .models import *
from django.db import transaction


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
    comments = CommentSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True)
    

    class Meta:
        model = Product
        fields = '__all__'
    def get_collection_name(self, obj):
        return obj.get_collection_name()
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newproduct_image = ProImage.objects.create(product=product, image=image)
        return product

    
class ClothesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clothes
        fields = '__all__'

     

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone', 'birth_date', 'membership', ]  

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'product','user')








class PanierItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = PanierItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price', 'subtotal']

class AddToPanierSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)





class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['id', 'user', 'items', 'created_at', 'total']
        read_only_fields = ['created_at', 'total']    

    
   
class ProductClothesChaussuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_clothes_chaussures
        fields = ('id', 'title', 'price', 'colors', 'src_image', 'alt_image', 'promotion_status', 'discount_percentage', 'quantity', 'pointure', 'description')
        