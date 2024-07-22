from django.shortcuts import render
from .models import (Product, ProductImages,
                     Brand, Review)
from django.views.generic import (ListView, DetailView)


# Create your views here.

class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product
