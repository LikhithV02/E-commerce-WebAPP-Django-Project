from django.contrib import admin
from .models import (
    category,
    customer,
    seller,
    orders,
    product,
    payment,
    warehouse,
    cart
)

@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name']

@admin.register(customer)
class customerAdmin(admin.ModelAdmin):
    list_display = ['user', 'c_name', 'email_id', 'mobile_no', 'c_add']

@admin.register(orders)
class ordersAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'pr_id', 'order_no', 'c_id']

@admin.register(payment)
class paymentAdmin(admin.ModelAdmin):
    list_display = ['pay_id', 'pay_type', 'order_no']

@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display = ['pr_id', 'pr_name', 'pr_price', 'pr_status', 'quantity',
    'description', 'pr_image', 'category_id', 'seller_id']

@admin.register(seller)
class sellerAdmin(admin.ModelAdmin):
    list_display = ['seller_id', 'seller_name', 'seller_add', 'GST_no',
    'seller_email_id', 'seller_mobile_no']

@admin.register(warehouse)
class warehouseAdmin(admin.ModelAdmin):
    list_display = ['pr_id', 'ware_pr_quantity', 'order_no']

@admin.register(cart)
class cartAdmin(admin.ModelAdmin):
    list_display = ['user','Product','order_no', 'order_date', 'order_quantity']