from django.db.models import Avg
from rest_framework import serializers
from .models import (Product, Brand, ProductImages,
                     Review)
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ['user', 'review', 'rate', 'created_at']


class ProductListSerializer(TaggitSerializer, serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    # count = serializers.SerializerMethodField(method_name='get_review_count') # if I want to name it 'count'
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['id', 'brand', 'name', 'review_count', 'avg_rate',
                  'flag', 'image', 'price', 'sku', 'subtitle',
                  'description', 'tags', 'slug']


class ProductDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    images = ProductImagesSerializer(source='product_image', many=True)
    reviews = ReviewSerializer(source='review_product', many=True)
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'flag', 'price', 'image', 'sku', 'subtitle', 'description',
                  'brand', 'review_count', 'avg_rate', 'images', 'reviews', 'tags']


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
