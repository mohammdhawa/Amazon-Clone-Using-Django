from django.urls import path
from .views import (ProductListView, ProductDetailView,
                    BrandListView, BrandDetailView)


urlpatterns = [
    path('brands', BrandListView.as_view(), name='brand-list'),
    path('brands/<slug:slug>', BrandDetailView.as_view(), name='brand-detail'),
    path('', ProductListView.as_view(), name='product-list'),
    path('<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
]
