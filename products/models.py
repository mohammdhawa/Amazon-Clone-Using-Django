from django.utils import timezone

from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

# Create your models here.

FLAG_TYPES = (
    ('New', 'New'),
    ('Feature', 'Feature'),
    ('Sale', 'Sale')
)

RATE_CHOICES = [(i, i) for i in range(1, 6)]


class Product(models.Model):
    name = models.CharField(max_length=100)
    flag = models.CharField(max_length=10, choices=FLAG_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/')
    sku = models.IntegerField()
    subtitle = models.TextField(max_length=400)
    description = models.TextField(max_length=50000)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)
    tags = TaggableManager()


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages')


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand')

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, related_name='review_user', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rate = models.IntegerField(choices=RATE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

