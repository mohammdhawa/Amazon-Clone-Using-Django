from rest_framework import pagination


class ProductPageNumberPagination(pagination.PageNumberPagination):
    page_size = 100

