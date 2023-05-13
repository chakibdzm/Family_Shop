from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from rest_framework import routers
from .views import *
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('Categories', views.CollectionViewSet)
router.register(r'clothes',views.ClotheViewSet)
router.register('favorites', FavoriteViewSet,basename='favorites')




# URLConf
urlpatterns = router.urls+[
    path('products/<int:product_id>',views.ProductDetail.as_view()),
    path('products/collection/<str:category_name>/', product_collection),
    path('clothes/collection/<str:category_name>/',views.ClotheViewSet.as_view({'get': 'clothes_collection'}), name='clothes-collection'),  
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'), 
    path('panier/', PanierItemList.as_view()),
    path('panier/add/', AddToPanier.as_view()),
    path('panier/remove/<int:product_id>/', RemoveFromPanier.as_view()),
    path('ordering/', OrderView.as_view(), name='order-list'),
    path('order/', UserOrderListView.as_view(), name='user-order-list'),
    
    
    ]

#end points are:
#ShopApp/products
#shopapp/products/prod_id ===> one prod
#shopapp/products/collection/colletion_id  ===>products in this category
#shopapp/collections ===> cateogry available

#search Queries
#ShopApp/products/?collection={collection_name} ====>filtering by collection
#ShopApp/products/?search={search_input} ===> search by title of prod


                

