from django.shortcuts import render
from .models import (Product, ProductImages,
                     Brand, Review)
from django.views.generic import (ListView, DetailView)


# Create your views here.

class ProductListView(ListView):
    model = Product
    paginate_by = 48


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.get_object())
        context['images'] = ProductImages.objects.filter(product=self.get_object())
        context['related'] = Product.objects.filter(brand=self.get_object().brand)[:10]
        return context


class BrandListView(ListView):
    model = Brand
    paginate_by = 50


# class BrandDetailView(DetailView):
#     model = Brand
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = Product.objects.filter(brand=self.get_object())
#         return context

class BrandDetailView(ListView):
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 5

    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset = super().get_queryset().filter(brand=brand)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = Brand.objects.get(slug=self.kwargs['slug'])
        return context
