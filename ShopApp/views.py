from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import action,api_view
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from rest_framework import status,generics
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .permissions import IsAdminOrReadOnly
from rest_framework import status
import jwt
from rest_framework.exceptions import AuthenticationFailed
from core.models import User

from rest_framework.parsers import MultiPartParser, FormParser

#

@api_view(['GET'])
def product_collection(request, category_name):
    category = get_object_or_404(Sub_collection, title=category_name)
    products = Product.objects.filter(collection=category)
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)



class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
    def perform_create(self, serializer):
        token = self.request.headers.get('Authorization', '').split(' ')[1]
        if not token:
            raise AuthenticationFailed('Unauthenticated! : no token found')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! token expired')

        user=User.objects.get(id=payload['id'])
        serializer.save(user=user)

'''
class ClothesViewSet(ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
     
    def clothes_collection(self, request, category_name=None):
        category = get_object_or_404(Sub_collection, title=category_name)
        gender = request.query_params.get('gender')
        queryset = self.queryset.filter(collection=category)
        if gender:
            queryset = queryset.filter(gender=gender)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
'''

class ClothesViewSet(ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer


class ProductDetail(generics.RetrieveAPIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CategoryDetail(APIView):
    def get(self, request,category_id):
        try:
            category= Collection.objects.get(id=Collection.featured_product)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CollectionSerializer(category)
        return Response(serializer.data)
    


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends=(DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields=['collection']
    permission_classes=[IsAdminOrReadOnly]

    #
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': "Product cannot be deleted because it is associated with an order item"},status=405)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes=[IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')),
            pk=kwargs['pk'])
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it contains products'},status=405)
        return super().destroy(request, *args, **kwargs)  
 


    
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]

  

    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created)=Customer.objects.get_or_create(user_id=request.user.id)
        if request.method=='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


 
    
    
class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer

    http_method_names=['get','post','delete']
    def get_queryset(self):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']
        favorites = Favorite.objects.filter(user_id=user_id)

        id = self.kwargs.get('id')
        if id:
            favorites = favorites.filter(id=id)
        return favorites
    
    def destroy(self, request, *args, **kwargs):
        
        product_id = self.kwargs.get('product_id')
        if not product_id:
            raise NotFound()

        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']

        favorites = Favorite.objects.filter(user_id=user_id, product_id=product_id)
        if not favorites.exists():
            raise NotFound()

        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


        
class panierViewSet(ModelViewSet):
    serializer_class=PanierItemSerializer
    http_method_names=['get','delete','put']
    def get_queryset(self):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']
        panier = PanierItem.objects.filter(user_id=user_id)

        id = self.kwargs.get('id')
        if id:
            panier = panier.filter(id=id)

        return panier
    
    def destroy(self, request, *args, **kwargs):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']
        queryset = PanierItem.objects.filter(user_id=user_id)

        id_prod = kwargs.get('id')
        if not id_prod:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=id_prod)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        panier_item = queryset.filter(product=product).first()
        if panier_item is None:
            return Response({'error': 'Product not found in panier.'}, status=status.HTTP_404_NOT_FOUND)

        panier_item.delete()
        return Response({'success': 'Product removed from panier.'}, status=status.HTTP_204_NO_CONTENT)
    
    
    def update(self, request, *args, **kwargs):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']
        queryset = PanierItem.objects.filter(user_id=user_id)

        id_prod = kwargs.get('id')
        if not id_prod:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=id_prod)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        panier_item = queryset.filter(product=product).first()
        if panier_item is None:
            return Response({'error': 'Product not found in panier.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(panier_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class AddToPanier(generics.CreateAPIView):
    serializer_class = AddToPanierSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']
        price = product.price
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()

        
        cart_item, created = PanierItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity, 'price': price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
class OrderView(APIView):
   

    def post(self, request):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated !')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated !')    

        user = User.objects.get(id=payload['id'])
        cart_items = PanierItem.objects.filter(user=user)
        order = Orders.objects.create(user=user)
        order.items.set(cart_items)
        order_serializer = OrdersSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)  

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self):
        token = self.request.headers.get('Authorization', '').split(' ')[1]

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user_id = payload['id']
        order = Orders.objects.filter(user_id=user_id)

        id = self.kwargs.get('id')
        if id:
            order = order.filter(id=id)

        return order
    
       

    
class ShopappProductClothesChaussuresViewSet(ModelViewSet):
    serializer_class = ProductClothesChaussuresSerializer
    queryset = product_clothes_chaussures.objects.all()      
