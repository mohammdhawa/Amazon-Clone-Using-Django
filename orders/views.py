from django.shortcuts import render, redirect
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
