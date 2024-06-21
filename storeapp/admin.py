from django.contrib import admin
from . models import *


# Register your models here.
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status']
    list_display = ['user','price', 'paid_status', 'order_date', 'product_status']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address','status']
    list_display = ['user', 'address', 'status']

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Address)
admin.site.register(WishList)
admin.site.register(ProductReview)
