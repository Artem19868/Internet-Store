from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_added')
    list_per_page = 20
    list_max_show_all = 100

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'amount', 'is_active')
    list_per_page = 20
    list_max_show_all = 100

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)