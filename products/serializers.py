from functools import reduce

from rest_framework import serializers

from .models import (Product, Brand, ProductImages, Review)



class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ['image']



class ProductReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['user', 'review', 'rate', 'created_at']



class ProductListSerializer(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()
    count_reviews = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"
    
    def get_count_reviews(self, object):
        reviews = object.review_roduct.count()
        return reviews

    def get_average_rate(self, object):
        reviews = object.review_roduct.all()
        
        total = sum(item.rate for item in reviews)
        
        return format(total/len(reviews), ".1f") if reviews else 0 



class ProductDetailSerializer(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()
    count_reviews = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    images = ProductImageSerializer(source='product_image', many=True)
    reviews = ProductReviewSerializer(source='review_roduct', many=True)

    class Meta:
        model = Product
        fields = "__all__"
    
    def get_count_reviews(self, object):
        reviews = object.review_roduct.all().count()
        return reviews

    def get_average_rate(self, object):
        reviews = object.review_roduct.all()
        total = sum(item.rate for item in reviews)
        return format(total/len(reviews), ".1f") if reviews else 0 



class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"



class BrandDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"