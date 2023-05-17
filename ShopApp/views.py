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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
 

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    
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

    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    #permission_classes=[IsAuthenticated]
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    @action(detail=False,methods=['POST','PATCH'],permission_classes=[IsAuthenticated])
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    


class FavoriteList(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    queryset=Favorite.objects.all() 


class FavoriteDetail(generics.RetrieveDestroyAPIView):
    serializer_class = FavoriteSerializer
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Favorite.objects.all()

    


class OrderViewSet(ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset= Order.objects.prefetch_related('items__product').all()
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    #def destroy(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    if instance.is_deletable():
    #        self.perform_destroy(instance)
    #        return Response(status=status.HTTP_204_NO_CONTENT)
    #    else:
    #        return Response({'detail': 'This order cannot be deleted.'}, status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
 

    
class ShopappProductClothesChaussuresViewSet(ModelViewSet):
    serializer_class = ProductClothesChaussuresSerializer
    queryset = product_clothes_chaussures.objects.all()      