from django.utils import timezone

from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify

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
    slug = models.SlugField(unique=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # check for uniqueness
            original_slug = self.slug
            queryset = Product.objects.filter(slug=original_slug)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
                queryset = Product.objects.filter(slug=self.slug)
        super(Product, self).save(*args, **kwargs)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages')


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brand')
    slug = models.SlugField(unique=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # check for uniqueness
            original_slug = self.slug
            queryset = Product.objects.filter(slug=original_slug)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
                queryset = Product.objects.filter(slug=self.slug)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, related_name='review_user', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)
    rate = models.IntegerField(choices=RATE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

