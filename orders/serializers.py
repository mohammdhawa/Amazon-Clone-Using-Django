from rest_framework import serializers

from .models import (Order, OrderDetail,
                     Cart, CartDetail)


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_detail = CartDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'coupon',
                  'total_with_coupon', 'cart_total']
