from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from BooksApp.filters import BookFilter, CustomPageNumberPagination
from BooksApp.models import Book
from BooksApp.permissions import CustomObjectPermissions
from BooksApp.serializers import BookSerializer, BookListSerializer


class BookViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                  GenericViewSet):
    """
    This viewset is responsible for handling operations related to books.
    Authentication is handled through JWT tokens and is covered by
    "rest_framework_simplejwt.authentication.JWTAuthentication".
    """
    permission_classes = [IsAuthenticated, CustomObjectPermissions]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    throttle_scope = "books"

    def get_serializer_class(self) -> BookSerializer:
        if self.action == "list":
            return BookListSerializer
        return BookSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=serializer.validated_data["user"])
        return Response(data=[], status=status.HTTP_201_CREATED)
