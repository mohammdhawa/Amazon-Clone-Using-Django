from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import datetime

from django.contrib.auth.models import User


from .serializers import (OrderSerializer, OrderDetailSerializer,
                          CartSerializer, CartDetailSerializer)
from .models import (Order, OrderDetail,
                     Cart, CartDetail, Coupon)
from products.models import Product
from settings.models import DeliveryFee
from accounts.models import Adress


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    # def get_queryset(self):
    #     queryset = super(OrderListAPI, self).get_queryset()
    #
    #     user = User.objects.get(username=self.kwargs['username'])
    #
    #     queryset = queryset.filter(user=user)
    #
    #     return queryset

    def list(self, request, *args, **kwargs):
        queryset = super(OrderListAPI, self).get_queryset()
        user = User.objects.get(username=self.kwargs['username'])
        queryset = queryset.filter(user=user)
        data = OrderSerializer(queryset, many=True).data
        return Response({'orders': data})


class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ApplyCouponAPI(generics.GenericAPIView):

    def post(self, request, *args, **kwargs): # function receive post request
        user = User.objects.get(username=self.kwargs['username']) # url
        coupon = get_object_or_404(Coupon, code=request.data['coupon_code']) # request body
        delivery_fee = DeliveryFee.objects.last().fee
        cart = Cart.objects.get(user=user, status='Inprogress')

        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            if coupon.start_date <= today_date <= coupon.end_date:
                coupon_value = cart.cart_total / 100 * coupon.discount
                sub_total = cart.cart_total - coupon_value

                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()

                coupon.quantity -= 1
                coupon.save()

                return Response({'message': "Coupon applied Successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Coupon is Invalid or Expired!"})
        else:
            return Response({'message': "Coupon is Not Found!"})


class CreateOrderAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        code = request.data['payment_code']
        address_id = request.data['address_id']

        user_address = Adress.objects.get(id=address_id)

        cart = Cart.objects.get(user=user, status='Inprogress')
        cart_detail = CartDetail.objects.filter(cart=cart)

        # cart: order | cart_detail: order_detail
        new_order = Order.objects.create(
            user=user,
            status='Received',
            code=code,
            delivery_address=user_address,
            coupon=cart.coupon,
            total_with_coupon=cart.total_with_coupon,
            total=cart.cart_total
        )

        # order detail
        for item in cart_detail:
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create(
                order=new_order,
                product=product,
                quantity=item.quantity,
                price=product.price,
                total_price=round(item.quantity * product.price, 2),
            )

            # Decrease product quantity
            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.quantity
            product.save()

        # Close cart
        cart.status = 'Completed'
        cart.save()

        # Send Email
        return Response({'message': "Order Created Successfully!"}, status=status.HTTP_201_CREATED)


class CartCreateUpdateDeleteAPI(generics.GenericAPIView):
    pass

