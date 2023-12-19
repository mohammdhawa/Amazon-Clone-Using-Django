from rest_framework import serializers

from .models import Product, Brand


class ProductListSerializer(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()
    count_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"
    
    def get_count_reviews(self, object):
        reviews = object.review_roduct.count()
        return reviews



class ProductDetailSerializer(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()
    count_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
    
    def get_count_reviews(self, object):
        reviews = object.review_roduct.count()
        return reviews



class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"



class BrandDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"