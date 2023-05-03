from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import *
from .serializers import *
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

#
@api_view(['GET'])
def product_by_category(request, collection_id):
    products = Product.objects.filter(collection_id=collection_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



class ClothesDetail(APIView):
    def get(self, request, gender_title):
        try:
            product = Clothes.objects.get(gender=gender_title)
        except Clothes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ClothesSerializer(product)
        return Response(serializer.data)




class ProductDetail(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class ClothesViewSet(ModelViewSet):
    queryset=Clothes.objects.all()
    serializer_class=ClothesSerializer
    filter_backends=(DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields=['gender']
    

    def get_serializer_context(self):
        return {'request': self.request}

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
    filter_backends=(DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields=['collection']
    search_fields=['tags','title']
    OrderingFilter=['price_with_tax']
    permission_classes=[IsAdminOrReadOnly]
    #
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

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    #@action(detail=False,methods=['POST','PATCH'],permission_classes=[IsAuthenticated])
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    
 
class ReviewViewSet(ModelViewSet):
    queryset = review.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
 

class FavoriteViewSet(ModelViewSet):
   # permission_classes = [IsAuthenticated] || user can add to fav without acc
    serializer_class = FavListSerializer
    queryset = favList.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddFavSerializer
        return FavListSerializer
    
    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(Product, id=product_id)
        favorite = get_object_or_404(favList, user=request.user, product=product)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

