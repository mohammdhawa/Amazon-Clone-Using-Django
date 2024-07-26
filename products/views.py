from django.shortcuts import render
from .models import (Product, ProductImages,
                     Brand, Review)
from django.views.generic import (ListView, DetailView)
from django.db.models import (Q, F, Avg, Count, Sum,
                              Min, Max, Value)
from django.views.decorators.cache import cache_page


# @cache_page(60 * 2)
def mydebug(request):

    data = Product.objects.all()

    # Columns with numeric data
    # data = Product.objects.filter(price=20)
    # data = Product.objects.filter(price > 90)  # This is not valid
    # data = Product.objects.filter(price__gt = 90) # here the correct way to return all products with price greater than 90
    # data = Product.objects.filter(price__gte = 90) # greater than or equal
    # data = Product.objects.filter(price__lt = 20) # less than
    # data = Product.objects.filter(price__lte = 20) # less than or equal
    # data = Product.objects.filter(price__range=(80, 83)) # prices which are between 80 and 83

    # Relation
    # data = Product.objects.filter(brand__id=3) # here when I write brand__ so now I'm in brand object(table)
    # data = Product.objects.filter(brand__id__lt=3) # here we want all products that their brand (brand id less than 5)

    # Text
    # data = Product.objects.filter(name__contains='tod') # it will return all products that their name has this text...
    # data = Product.objects.filter(name__startswith='tod')
    # data = Product.objects.filter(name__endswith='thomas')
    # data = Product.objects.filter(price__isnull=True)

    # Dates
    # data = Product.objects.filter(date_column__year=2022)
    # data = Product.objects.filter(data_column__month=2)
    # data = Product.objects.filter(data_column__day=2)

    # Complex Query
    # data = Product.objects.filter(flag='New', price__gt=98)
    # data = Product.objects.filter(flag='New').filter(price__gt=98) # same of the above query
    # data = Product.objects.filter(
    #     Q(flag='New') |
    #     Q(price__gt=98)
    # )
    # data = Product.objects.filter(
    #     ~ Q(flag='New') |
    #     Q(price__gt=98)
    # )

    # Field Reference
    '''
    useful for performing database operations that involve comparisons, 
    updates, or annotations without bringing data into Python's memory space.
    '''
    # Comparing Fields within a Query
    # data = Product.objects.filter(quantity=F('price')) # bring all products that their quantity equal their price
    # data = Product.objects.filter(quantity=F('category__id')) # where quantity = category id
    # Updating a Field Based on Its Current Value
    # Product.objects.update(price=F('price') * 1.1)

    # Order
    # data = Product.objects.all().order_by('name')
    # data = Product.objects.order_by('name')
    # data = Product.objects.order_by('-name') # DES
    # data = Product.objects.order_by('-name', 'price')
    # data = Product.objects.order_by('name')[:10]
    # data = Product.objects.earliest('name') # return the first one
    # data = Product.objects.latest('name') # return the last one

    # Limit Fields
    # data = Product.objects.values('name', 'price') # to choose the columns we want
    # data = Product.objects.values_list('name', 'price') # same of above line but it return them as a tuple
    # data = Product.objects.only('name', 'price') # same of values
    # data = Product.objects.defer('description') # excludes the column we doesn't want

    # Select Related  --- very powerfull
    '''
    used to create a SQL join and include the fields of the related object in the SELECT statement. 
    This can be useful for accessing related objects efficiently, reducing the number of database 
    queries by performing a single, more complex query instead of multiple simpler ones.
    '''
    # data = Product.objects.select_related('brand').all() # used with ForiegnKey, one-to-one
    # data = Product.objects.prefetch_related('brand').all() # used with many-to-many

    # Aggregation: count, min, max, sum, avg
    '''
    allows you to perform database-level calculations, such as summing values, averaging, 
    counting, etc., directly in your queries. This can be very efficient and useful for 
    generating reports and summaries.
    '''
    # data = Product.objects.aggregate(Avg('price')) # price Average
    # data = Product.objects.aggregate(Sum('price'))
    # data = Product.objects.aggregate(Count('id'))
    # data = Product.objects.aggregate(Min('price'))
    # data = Product.objects.aggregate(Max('price'))
    # data = Product.objects.aggregate(price_avg=Avg('price')) # naming it /price_avg'
    # data = Product.objects.aggregate(
    #     myavg=Avg('price'),
    #     mycount=Count('id')
    # )

    # Annotation
    '''
    used to add aggregate values to each item in a queryset. This can be useful for 
    performing calculations on related data and appending the result as an extra 
    field to each instance of the queryset.
    '''
    # data = Product.objects.annotate(is_new=Value(0))
    # data = Product.objects.annotate(price_with_tax=F('price')*1.2)

    return render(request, 'products/debug.html', {'data': data})


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
    queryset = Brand.objects.annotate(product_count=Count('product_brand'))


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
        context['brand'] = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_brand'))[0]
        return context
