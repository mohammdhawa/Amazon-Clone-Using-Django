from django.utils import timezone

from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.

FLAG_TYPES = (
    ('New', 'New'),
    ('Feature', 'Feature'),
    ('Sale', 'Sale')
)

RATE_CHOICES = [(i, i) for i in range(1, 6)]


class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    flag = models.CharField(_('flag'), max_length=10, choices=FLAG_TYPES)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    image = models.ImageField(_('image'), upload_to='product/')
    sku = models.IntegerField(_('sku'), unique=True)
    subtitle = models.TextField(_('subtitle'), max_length=400)
    description = models.TextField(_('description'), max_length=50000)
    brand = models.ForeignKey('Brand', verbose_name=_('brand'), related_name='product_brand', on_delete=models.SET_NULL, null=True)
    tags = TaggableManager()
    # quantity =
    slug = models.SlugField(unique=True, max_length=100, blank=True)

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

    def __str__(self):
        return self.name

    def review_count(self):
        reviews = self.review_product.all().count()
        return reviews

    def avg_rate(self):
        reviews = self.review_product.all()

        if not reviews:
            return 0

        total = sum(review.rate for review in reviews)
        avg = round(total / len(reviews), 1)

        return avg

    class Meta:
        ordering = ['-id']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='product_image', on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='productimages')


class Brand(models.Model):
    name = models.CharField(_('name'), max_length=100)
    image = models.ImageField(_('image'), upload_to='brand')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # check for uniqueness
            original_slug = self.slug
            queryset = Brand.objects.filter(slug=original_slug)
            count = 1
            while queryset.exists():
                self.slug = f"{original_slug}-{count}"
                count += 1
                queryset = Brand.objects.filter(slug=self.slug)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='review_user', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name=_('product'), related_name='review_product', on_delete=models.CASCADE)
    review = models.TextField(_('review'), max_length=1000)
    rate = models.IntegerField(_('rate'), choices=RATE_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.rate}"

