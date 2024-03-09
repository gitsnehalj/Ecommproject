from django.contrib import admin

from .models import product
from .models import Cart
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
      list_display=['id','name','price','pdetails','cat','is_active','pimage']
      list_filter=['cat','is_active']
class CartAdmin(admin.ModelAdmin):
      list_display=['id','uid','pid']     
admin.site.register(product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
