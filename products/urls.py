from django.urls import path

from .views import (ProductList, ProductDetail,
                    BrandList)


urlpatterns = [
    path('', ProductList.as_view(), name='products'),
    path('brand/', BrandList.as_view(), name='brand_list'),
    path('<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
]
