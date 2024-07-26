from django.db.models import Avg
from rest_framework import serializers
from .models import (Product, Brand, ProductImages,
                     Review)


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ['user', 'review', 'rate', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    # count = serializers.SerializerMethodField(method_name='get_review_count') # if I want to name it 'count'
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        reviews = object.review_count()
        return reviews

    def get_avg_rate(self, object):
        avg = object.avg_rate()
        return avg


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    images = ProductImagesSerializer(source='product_image', many=True)
    reviews = ReviewSerializer(source='review_product', many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        reviews = object.review_count()
        return reviews

    def get_avg_rate(self, object):
        avg = object.avg_rate()
        return avg


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
