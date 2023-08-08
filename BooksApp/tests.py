from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from model_bakery.baker import make
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from BooksApp.models import Book
from BooksApp.serializers import BookSerializer
from UsersApp.models import User
from utils import BaseTestCase, Errors


class BooksTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_without_permission = make(User)
        self.data = {"title": "title", "author": "test", "user": self.user}
        self.book = make(Book, **self.data)
        self.administrator_refresh_token = RefreshToken.for_user(self.user)
        self.token = str(self.administrator_refresh_token.access_token)

    def _create_book(self):
        response = self.client.post(reverse("books-list"), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_with_good_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.data = {"title": "title", "author": "test", "user": self.user.id}
        response = self.client.post(reverse("books-list"), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def _create_book_for_permissions_testing_purposes(self):
        self.data["user"] = self.user_without_permission.pk
        serializer = BookSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        if not self.user_without_permission.has_perm("auth.add_book"):
            raise PermissionDenied("You do not have permission to create a book.")
        serializer.save(user=self.user_without_permission)
        return Response(data=[], status=status.HTTP_201_CREATED)

    def test_create_book_without_permission(self):
        self.client.force_authenticate(self.user_without_permission)
        refresh = RefreshToken.for_user(self.user_without_permission)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        with self.assertRaises(PermissionDenied):
            self._create_book_for_permissions_testing_purposes()

    def test_get_books_without_permission(self):
        self.client.force_authenticate(self.user_without_permission)
        refresh = RefreshToken.for_user(self.user_without_permission)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("books-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], Errors.PERMISSION_DENIED)

    def test_delete_book_without_permission(self):
        self.client.force_authenticate(self.user_without_permission)
        refresh = RefreshToken.for_user(self.user_without_permission)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.delete(reverse("books-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], Errors.PERMISSION_DENIED)

    def test_retrieve_own_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        book_data = {"title": "title", "author": "author", "user": self.user.id}
        response = self.client.post(reverse("books-list"), data=book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(title="title", author="author", user=self.user)
        book_id = book.id
        response = self.client.get(reverse("books-detail", args=[book_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_book(self):
        self.client.force_authenticate(self.user_without_permission)
        refresh = RefreshToken.for_user(self.user_without_permission)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("books-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], Errors.PERMISSION_DENIED)

    def test_retrieve_other_user_book_with_administrator_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(reverse("books-detail", args=[self.book.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)
        self.assertEqual(response.data["author"], self.book.author)
        self.assertEqual(response.data["publication_date"], self.book.publication_date)
        self.assertEqual(response.data["user"], self.user.id)


class BookPaginationTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = make(User)
        self.books = [make(Book, title=f"title{i}", author="author", user=self.user) for i in range(20)]
        self.client.force_authenticate(user=self.user)
        self.url = reverse("books-list")
        permissions = Permission.objects.filter(codename__in=["add_book", "delete_book", "change_book", "view_book"])
        self.user.user_permissions.add(*permissions)

    def test_pagination_with_items_per_page_5(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, data={"items_per_page": 5, "page_number": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_pagination_with_items_per_page_4(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, data={"items_per_page": 4, "page_number": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)
