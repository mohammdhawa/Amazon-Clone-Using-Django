from django.shortcuts import render
from .models import (Order, OrderDetail, Cart,
                     CartDetail, Coupon)

# Create your views here.

def order_list(request):
    data = Order.objects.all()

    return render(request, 'orders/order_list.html', {'data': data})
