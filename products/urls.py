from django.urls import path
from .views import (ProductListView, ProductDetailView,
                    BrandListView, BrandDetailView)
from . import api


urlpatterns = [
    path('brands', BrandListView.as_view(), name='brand-list'),
    path('brands/<slug:slug>', BrandDetailView.as_view(), name='brand-detail'),
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),

    # api urls
    path('api/list', api.ProductListAPI.as_view(), name='product-list-api'),
    path('api/list/<int:pk>', api.ProductDetailAPI.as_view(), name='product-detail-api'),
    path('api/brands', api.BrandListAPI.as_view(), name='brand-list-api'),
    path('api/brands/<int:pk>', api.BrandDetailAPI.as_view(), name='brand-detail-api'),
]
