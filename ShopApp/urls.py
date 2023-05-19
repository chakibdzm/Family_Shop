from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from rest_framework import routers
from .views import *
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('Categories', views.CollectionViewSet)
router.register('favorites', FavoriteViewSet,basename='favorites')
router.register('panier',views.panierViewSet,basename='panier')
router.register(r'clothes',views.ClothesViewSet)
router.register(r'product_clothes_chaussures', ShopappProductClothesChaussuresViewSet)



# URLConf
urlpatterns = router.urls+[
    path('products/<int:product_id>',views.ProductDetail.as_view()),
    path('products/collection/<str:category_name>/', product_collection),

    #path('clothes/collection/<str:category_name>/',views.ClotheViewSet.as_view({'get': 'clothes_collection'}), name='clothes-collection'),  
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'), 
    path('panier_add/', AddToPanier.as_view()),
    path('panier_remove/<int:id>/', panierViewSet.as_view({'delete': 'destroy'})),
    path('panier_update/<int:id>/', panierViewSet.as_view({'put': 'update'})),
    path('ordering/', OrderView.as_view(), name='order-list'),
    path('order/', UserOrderListView.as_view(), name='user-order-list'),
    path('favorites_remove/<int:product_id>/', FavoriteViewSet.as_view({'delete': 'destroy'}), name='favorite-delete'),
    path('clothes/collection/<str:category_name>/',views.ClothesViewSet.as_view({'get': 'clothes_collection'}), name='clothes-collection'),  
  
    
    ]

#end points are:
#ShopApp/products
#shopapp/products/prod_id ===> one prod
#shopapp/products/collection/colletion_id  ===>products in this category
#shopapp/collections ===> cateogry available

#search Queries
#ShopApp/products/?collection={collection_name} ====>filtering by collection
#ShopApp/products/?search={search_input} ===> search by title of prod


                

