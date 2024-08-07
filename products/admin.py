from django.contrib import admin
from .models import Product, Brand, Review, ProductImages


# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 4


class ProductImagesAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]
    search_fields = ['name', 'sku']
    list_filter = ['flag']


admin.site.register(Product, ProductImagesAdmin)
admin.site.register(Brand)
admin.site.register(Review)
