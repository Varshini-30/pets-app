from django.contrib import admin
from .models import Pet, Order, OrderItem, Customer, ShippingAddress1
# Register your models here.

#  admin.site.register(Pet)


class Petadmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'gender',
                    'breed', 'description', 'price')


admin.site.register(Pet, Petadmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id')


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')


admin.site.register(OrderItem, OrderItemAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')


admin.site.register(Customer, CustomerAdmin)


class ShippinAddress1Admin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'city',
                    'state', 'zipcode', 'date_added')


admin.site.register(ShippingAddress1)
