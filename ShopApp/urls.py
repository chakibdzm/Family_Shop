from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from rest_framework import routers
from .views import *
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('Categories', views.CollectionViewSet)
<<<<<<< HEAD
router.register(r'clothes',views.ClotheViewSet)
=======
>>>>>>> 19a84659995c57edd16ba38b67dc12e36fba4f21
router.register('favorites', FavoriteViewSet,basename='favorites')
router.register('panier',views.panierViewSet,basename='panier')

router.register(r'clothes',views.ClothesViewSet)
router.register(r'product_clothes_chaussures', ShopappProductClothesChaussuresViewSet)



# URLConf
urlpatterns = router.urls+[
    path('products/<int:product_id>',views.ProductDetail.as_view()),
    path('products/collection/<str:category_name>/', product_collection),
<<<<<<< HEAD
    path('clothes/collection/<str:category_name>/',views.ClotheViewSet.as_view({'get': 'clothes_collection'}), name='clothes-collection'),  
=======

    #path('clothes/collection/<str:category_name>/',views.ClotheViewSet.as_view({'get': 'clothes_collection'}), name='clothes-collection'),  
>>>>>>> 19a84659995c57edd16ba38b67dc12e36fba4f21
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'), 
    path('panier_add/', AddToPanier.as_view()),
    path('panier_remove/<int:id>/', panierViewSet.as_view({'delete': 'destroy'})),
    path('panier_update/<int:id>/', panierViewSet.as_view({'put': 'update'})),
    path('ordering/', OrderView.as_view(), name='order-list'),
    path('order/', UserOrderListView.as_view(), name='user-order-list'),
    path('favorites_remove/<int:product_id>/', FavoriteViewSet.as_view({'delete': 'destroy'}), name='favorite-delete'),
<<<<<<< HEAD
    path('clothes/collection/<str:category_name>/',views.ClothesViewSet.as_view({'get': 'clothes_collection'}), name='clothes-collection'),  
  
=======
    path('notifications/', UserNotificationView.as_view(),basename='user-notifications'),
>>>>>>> cbf91b15f5b3b813dc3d21abed20e5e50303db0a
    
    ]

#end points are:
#ShopApp/products
#shopapp/products/prod_id ===> one prod
#shopapp/products/collection/colletion_id  ===>products in this category
#shopapp/collections ===> cateogry available

#search Queries
#ShopApp/products/?collection={collection_name} ====>filtering by collection
#ShopApp/products/?search={search_input} ===> search by title of prod


                

