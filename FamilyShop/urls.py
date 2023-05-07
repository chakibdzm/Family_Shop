#from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from core.views import LoginView, LogoutView, RegisterView, UserView

#admin.site.site_header = 'Family Shop'
#admin.site.index_title = 'Admin'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('ShopApp/', include('ShopApp.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

router = DefaultRouter()
router.register(r'users', UserViewSet)

# JWT Token urls
urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Djoser urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user', UserView.as_view())
]

# User urls
urlpatterns += router.urls

   
