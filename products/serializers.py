from django.db.models import Avg
from rest_framework import serializers
from .models import (Product, Brand)


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    # count = serializers.SerializerMethodField(method_name='get_review_count') # if I want to name it 'count'
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        reviews = object.review_product.all().count()
        return reviews

    def get_avg_rate(self, obj):
        reviews = obj.review_product.all()

        if not reviews:
            return 0

        total = sum(review.rate for review in reviews)
        avg = round(total / len(reviews), 1)

        return avg


class ProductDetailSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_review_count(self, object):
        reviews = object.review_product.all().count()
        return reviews

    def get_avg_rate(self, obj):
        reviews = obj.review_product.all()

        if not reviews:
            return 0

        total = sum(review.rate for review in reviews)
        avg = round(total / len(reviews), 1)

        return avg


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
