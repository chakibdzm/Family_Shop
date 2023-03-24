from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)

carts_router = NestedDefaultRouter(router, 'carts', lookup = 'cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + carts_router.urls