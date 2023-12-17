from typing import Any
from django.db import models
from django.shortcuts import render

from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)


from .models import (Product, Brand, Review, ProductImages)


class ProductList(ListView):
    model = Product
    paginate_by = 50



class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.get_object())
        context["images"] = ProductImages.objects.filter(product=self.get_object())
        context["related"] = Product.objects.filter(brand=self.get_object().brand)
        
        return context



class BrandList(ListView):
    model = Brand
    paginate_by = 50

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    


class BrandDetail(ListView):
    model = Product
    paginate_by = 10
    template_name = 'products/brand_detail.html'


    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        query_set = super().get_queryset().filter(brand=brand)
        return query_set
    

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['brand'] = Brand.objects.get(slug=self.kwargs['slug'])
        # print(context)
        return context
    