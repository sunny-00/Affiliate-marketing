from django.contrib import admin
from ecomapp.models import Product,Category,Login_Info,Orders,RefferedOrders,DetailOrder,Cart
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','qty','category_code','status','in_stock','promoting_link','promoting_status','pimage']
    list_filter=['category_code','status','in_stock']
    ordering = ('price','qty')
admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['code','category','promoting_percent','status','promoting_status']
    list_filter=['promoting_status','status']
admin.site.register(Category,CategoryAdmin)

class Login_Info_Admin(admin.ModelAdmin):
    list_display=['firstname','lastname','email','password','referral_id','address']
admin.site.register(Login_Info,Login_Info_Admin)

class OrdersAdmin(admin.ModelAdmin):
    list_display=['ordernumber','purchased_email','if_reffered','price','qty','status']
admin.site.register(Orders,OrdersAdmin)

class RefferedOrdersAdmin(admin.ModelAdmin):
    list_display=['ordernumber','referral_id','comission_amt','status']
admin.site.register(RefferedOrders,RefferedOrdersAdmin)

class DetailOrderAdmin(admin.ModelAdmin):
    list_display=['ordernumber','product_id']
admin.site.register(DetailOrder,DetailOrderAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['pid','uid']
admin.site.register(Cart,CartAdmin)