from django.shortcuts import render
from .models import (Product, ProductImages,
                     Brand, Review)
from django.views.generic import (ListView, DetailView)


# Create your views here.

class ProductListView(ListView):
    model = Product


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


class BrandDetailView(DetailView):
    pass
