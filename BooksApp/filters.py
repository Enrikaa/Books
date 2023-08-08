from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from BooksApp.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    date_from = filters.DateFilter(field_name="publication_date", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="publication_date", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["title", "publication_date"]


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = "page_number"
    page_size_query_param = "items_per_page"

