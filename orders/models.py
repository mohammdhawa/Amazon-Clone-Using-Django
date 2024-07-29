from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from products.models import Product
from utils.generate_code import generate_code
from accounts.models import Adress

ORDER_STATUS_CHOICES = (
    ('Received', 'Received'),
    ('Processed', 'Processed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered')
)


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_owner', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=12, choices=ORDER_STATUS_CHOICES)
    code = models.CharField(default=generate_code, unique=True, max_length=8)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_address = models.ForeignKey(Adress, related_name='delivery_address', on_delete=models.SET_NULL, null=True)
    coupon = models.ForeignKey('Coupon', related_name='order_coupon', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    total_with_coupon = models.FloatField(null=True, blank=True)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_detail_product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)


CART_STATUS_CHOICES = (
    ('Inprogress', 'Inprogress'),
    ('Completed', 'Completed'),
)


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart_owner', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=12, choices=CART_STATUS_CHOICES)
    coupon = models.ForeignKey('Coupon', related_name='cart_coupon', on_delete=models.SET_NULL, null=True, blank=True)
    total_with_coupon = models.FloatField(null=True, blank=True)


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_detail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_detail_product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.FloatField(null=True, blank=True)


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    quantity = models.IntegerField()
    discount = models.FloatField()

    def save(self, *args, **kwargs):
        week = timezone.timedelta(days=7)
        self.end_date = self.start_date + week
        super(Coupon, self).save(*args, **kwargs)
