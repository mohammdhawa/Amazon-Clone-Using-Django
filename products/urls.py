from django.urls import path

from .views import (ProductList, ProductDetail,
                    BrandList, BrandDetail)


urlpatterns = [
    path('', ProductList.as_view(), name='products'),
    path('brands/', BrandList.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetail.as_view(), name='brand_detail'),
    path('<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
]
