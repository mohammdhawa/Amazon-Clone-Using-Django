from django.urls import path
from .views import order_list, checkout, add_to_cart
from .api import OrderListAPI, OrderDetailAPI


urlpatterns = [
    path('', order_list, name='order_list'),
    path('checkout', checkout, name='checkout'),
    path('add_to_cart', add_to_cart, name='add_to_cart'),

    # API urls
    path('api/<str:username>/orders', OrderListAPI.as_view(), name='order_list_api'),
    path('api/<str:username>/orders/<int:pk>', OrderDetailAPI.as_view(), name='order_detail_api'),
]
