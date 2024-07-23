from rest_framework import generics
from .models import (Product, Brand, Review, ProductImages)
from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          BrandListSerializer, BrandDetailSerializer)
from .pagination import ProductPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = ProductPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['flag', 'brand']
    search_fields = ['name', 'sku']


class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer


class BrandDetailAPI(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
