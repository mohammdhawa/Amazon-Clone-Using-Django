from django.contrib import admin

from .models import Product, Brand, Review, ProductImages

# Register your models here.

class ProductImagesInline(admin.TabularInline):
    model = ProductImages


class ReviewProductInline(admin.TabularInline):
    model = Review

class ProductAdmin(admin.ModelAdmin):
   inlines = [ProductImagesInline, ReviewProductInline]
   list_filter = ['id', 'name']





admin.site.register(Product, ProductAdmin)


# admin.site.register(Product)

admin.site.register(Brand)

admin.site.register(Review)

# admin.site.register(ProductImages)