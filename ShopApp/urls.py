from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from rest_framework import routers
from .views import *
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('customers', views.CustomerViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('clothes',views.ClothesViewSet)



carts_router = NestedDefaultRouter(router, 'carts', lookup = 'cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


# URLConf
urlpatterns = router.urls+carts_router.urls+[
    path('products/<int:product_id>',views.ProductDetail.as_view()),
    path('products/collection/<int:collection_id>/', product_by_category),
    
    ]

#end points are:
#ShopApp/products
#shopapp/products/prod_id ===> one prod
#shopapp/products/collection/colletion_id  ===>products in this category
#shopapp/collections ===> cateogry available

#search Queries
#ShopApp/products/?collection={collection_name} ====>filtering by collection
#ShopApp/products/?search={search_input} ===> search by title of prod


                

