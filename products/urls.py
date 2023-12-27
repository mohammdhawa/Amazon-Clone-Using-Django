from django.urls import path

from .views import (ProductList, ProductDetail,
                    BrandList, BrandDetail, mydebug)

from .api import (ProductListAPI, ProductDetailAPI,
                  BrandListAPI, BrandDetailAPI)


urlpatterns = [
    path('debug', mydebug, name='debug'),
    path('brands', BrandList.as_view(), name='brand_list'),
    path('brands/<slug:slug>', BrandDetail.as_view(), name='brand_detail'),
    path('', ProductList.as_view(), name='products'),
    path('<slug:slug>', ProductDetail.as_view(), name='product_detail'),

    # API
    path('api/list', ProductListAPI.as_view(), name='products_api'),
    path('api/list/<int:pk>', ProductDetailAPI.as_view(), name='product_detail_api'),
    path('api/brands', BrandListAPI.as_view(), name='brand_api'),
    path('api/brands/<int:pk>', BrandDetailAPI.as_view(), name='brand_detail_api'),
    
]
