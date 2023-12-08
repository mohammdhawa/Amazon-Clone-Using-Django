from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductList.as_view()),
    path('<slug:slug>/', views.ProductDetail.as_view()),
]
