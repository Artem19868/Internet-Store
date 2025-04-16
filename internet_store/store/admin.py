import admin_thumbnails
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductGallery

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('amount', 'price', 'product_name', 'category', 'is_available')
    search_fields = ('product_name', 'category__category_name')
    list_per_page = 20
    list_max_show_all = 100
    prepopulated_fields = {"slug": ("product_name",)}
    inlines = [ProductGalleryInline]

class ProductGallaryAddmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html('<img src="{}" width="40">'.format(obj.image.url))
    
    thumbnail.short_description = 'Product image'
    list_display = ('product','thumbnail')
    list_display_links = ('product', 'thumbnail')
    list_filter = ('product',)
    search_fields = ('product__product_name',)
    list_per_page = 20
    list_max_show_all = 100

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery, ProductGallaryAddmin)
