from django.contrib import admin
from django.urls import path, include
import debug_toolbar

admin.site.site_header = 'Family Shop'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ShopApp/', include('ShopApp.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]