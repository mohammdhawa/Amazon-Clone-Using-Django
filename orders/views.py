from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import datetime

from .models import (Order, OrderDetail, Cart,
                     CartDetail, Coupon)
from products.models import Product
from settings.models import DeliveryFee


# Create your views here.

def order_list(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'order_list': orders
    }
    return render(request, 'orders/order_list.html', context)


def checkout(request):
    cart = Cart.objects.get(user=request.user, status='Inprogress')
    cart_detail = CartDetail.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    if request.method == 'POST':
        code = request.POST['coupon_code']
        coupon = get_object_or_404(Coupon, code=code)

        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()
            if coupon.start_date <= today_date <= coupon.end_date:
                coupon_value = cart.cart_total / 100 * coupon.discount
                sub_total = cart.cart_total - coupon_value
                total = sub_total + delivery_fee

                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()

                coupon.quantity -= 1
                coupon.save()



                context = {
                    'cart_detail': cart_detail,
                    'delivery_fee': delivery_fee,
                    'sub_total': round(sub_total, 2),
                    'discount': round(coupon_value, 2),
                    'total': round(total, 2)
                }

                return render(request, 'orders/checkout.html', context)

    sub_total = cart.cart_total
    discount = 0
    total = sub_total + delivery_fee

    context = {
        'cart_detail': cart_detail,
        'delivery_fee': delivery_fee,
        'sub_total': sub_total,
        'discount': discount,
        'total': total
    }

    return render(request, 'orders/checkout.html', context)


def add_to_cart(request):
    product = Product.objects.get(id=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity'))

    cart = Cart.objects.get(
        user=request.user,
        status='Inprogress'
    )

    cart_detail, created = CartDetail.objects.get_or_create(cart=cart, product=product)
    cart_detail.quantity = quantity
    cart_detail.total_price = round(product.price * cart_detail.quantity, 2)
    cart_detail.save()

    return redirect('product-detail', slug=product.slug)
