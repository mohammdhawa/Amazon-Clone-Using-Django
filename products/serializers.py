from rest_framework import serializers
from .models import (Product, Brand)


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    # count = serializers.SerializerMethodField(method_name='get_review_count') # if I want to name it 'count'
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        reviews = object.review_product.all().count()
        return reviews


class ProductDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        reviews = object.review_product.all().count()
        return reviews


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
