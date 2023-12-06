from django.db import models

from taggit.managers import TaggableManager

from django.contrib.auth.models import User

from django.utils import timezone

from django.utils.text import slugify

from django.utils.translation import gettext_lazy as _

# Create your models here.

FLAG_TYPES = (
    ('New', 'New'),
    ('Sale', 'Sale'),
    ('Feature', 'Feature')
)

class Product(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=120)
    flag = models.CharField(verbose_name=_('flag'), max_length=50, choices=FLAG_TYPES)
    price = models.FloatField(verbose_name=_('price'), )
    image = models.ImageField(verbose_name=_('image'), upload_to='product')
    sku = models.IntegerField(verbose_name=_('sku'), )
    subtitle = models.TextField(verbose_name=_('subtitle'), max_length=500)
    description = models.TextField(verbose_name=_('description'), max_length=50000)
    brand = models.ForeignKey('Brand', verbose_name=_('brand'), related_name='product_brand', on_delete=models.SET_NULL)
    tags =TaggableManager()

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.name



class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('image'), upload_to='product_images')



class Brand(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100)
    image = models.ImageField(verbose_name=_('image'), upload_to='brand')

    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
    

    def __str__(self):
        return self.name



class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='review_user', on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='review_roduct', on_delete=models.CASCADE)
    review = models.TextField(verbose_name=_('review'), max_length=1000)
    rate = models.IntegerChoices(verbose_name=_('rate'), choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} - {self.product} - {self.rate}"