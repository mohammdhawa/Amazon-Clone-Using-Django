from typing import Any
from django.db import models
from django.shortcuts import render

from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)


from .models import (Product, Brand, Review, ProductImages)
from django.db.models import Q, F, Value
from django.db.models.aggregates import Count, Sum, Avg, Max, Min


def mydebug(request):
    # data = Product.objects.all()

    # column number  ------------------------------------
    # data = Product.objects.filter(price=20)
    # data = Product.objects.filter(price__gt = 98)
    # data = Product.objects.filter(price__gte=98)
    # data = Product.objects.filter(price__lt=25)
    # data = Product.objects.filter(price__lte=25)
    # data = Product.objects.filter(price__range=(80, 83))

    # Relation  ------------------------------------
    # data = Product.objects.filter(brand__id=545)
    # data = Product.objects.filter(brand__id__gt=545)

    # Text  ------------------------------------
    # data = Product.objects.filter(name__contains='Colon')
    # data = Product.objects.filter(name__startswith='Debra')
    # data = Product.objects.filter(name__endswith='Kelley')
    # data = Product.objects.filter(price__isnull=True)

    # Dates  ------------------------------------
    # data = Product.objects.filter(date_column__year=2022)
    # data = Product.objects.filter(date_column__month=2)
    # data = Product.objects.filter(date_column__day=20)

    # Complex queries  ------------------------------------
    # data = Product.objects.filter(flag='New', price__gt=98) # or we can write it in another way
    # data = Product.objects.filter(flag='New').filter(price__gt=98) # the second way to get the same output of the abouve line
    # in the above 2 lines we used "and" in db sql
    # what about if we need to use "or"??? 

    # data = Product.objects.filter(
    #     ~Q(flag='New') | # or ... if we need to be and we use &, ~ not
    #     Q(price__gt=98)
    # )

    # Field Reference  ------------------------------------
    # data = Product.objects.filter(quantity=F('price')) # give me the products that has quantity as their price
    # data = Product.objects.filter(quantity=F('category_id'))

    # Order  ------------------------------------
    # data = Product.objects.all().order_by('name') # or
    # data = Product.objects.order_by('name') # ASC
    # data = Product.objects.order_by('-name') # DESC
    # data = Product.objects.order_by('-name', 'price') # order first by name (desc) second by price (asc)

    # data = Product.objects.filter(price__gt=98).order_by('name')
    # data = Product.objects.order_by('name')[:10]
    # data = Product.objects.earliest('name') # order by name and get the first one
    # data = Product.objects.latest('name') # order by name and get the last one

    # Limit Fields  ------------------------------------
    # data = Product.objects.values('name', 'price')
    # data = Product.objects.values_list('name', 'price') # as tuple not dictionary
    # data = Product.objects.only('name', 'price') # as variables
    # data = Product.objects.defer('description', 'subtitle') # the columns tha I don't want them

    # Select Related  ------------------------------------ (important)
    # data = Product.objects.select_related('brand').all() # with ForiengnKey and ont-to-one relationships
    # data = Product.objects.prefetch_related('brand').all() # with many-to-many relationship
    # data = Product.objects.select_related('brand').select_related('category').all() # we can do that

    # Aggregation: Count, Min, Max, Sum, AVG
    # data = Product.objects.aggregate(myavg = Avg('price'),
    #                                  mycount=Count('id'))

    # Annotation (important)
    # data = Product.objects.annotate(is_new=Value(0)) # it creates a new column (which is not exist in db)
    data = Product.objects.annotate(price_with_tax=F('price')*1.15)

    return render(request, 'products/debug.html', {'data': data})



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
    