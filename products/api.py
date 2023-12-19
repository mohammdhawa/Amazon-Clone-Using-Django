from rest_framework import generics

from .serializers import (ProductListSerializer, ProductDetailSerializer,
                          BrandListSerializer, BrandDetailSerializer)
from .models import (Product, ProductImages,
                     Brand, Review)

from .pagination import MyPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'flag']
    search_fields = ['name', 'subtitle', 'description']



class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer



class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer

    pagination_class = MyPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



class BrandDetailAPI(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer