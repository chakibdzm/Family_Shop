from django.contrib import admin
from .models import *
from .models import Product

# Register your models here.




admin.site.register(Product,ProductAdmin)
admin.site.register(Collection)
admin.site.register(Sub_collection)
admin.site.register(Clothes)
admin.site.register(Orders)



