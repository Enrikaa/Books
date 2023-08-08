from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from BooksApp.models import Book
from UsersApp.examples import BOOK_LIST_PAYLOAD, BOOK_DETAIL_PAYLOAD


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User login example",
            value=BOOK_LIST_PAYLOAD,
            request_only=True,
        ),
    ]
)
class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User login example",
            value=BOOK_DETAIL_PAYLOAD,
            request_only=True,
        ),
    ]
)
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "publication_date", "user"]
