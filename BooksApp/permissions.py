from rest_framework import permissions
from rest_framework.request import Request

from BooksApp.models import Book


class CustomObjectPermissions(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if view.action == "create":
            return request.user.has_perm("BooksApp.add_book")
        elif view.action == "list":
            return request.user.has_perm("BooksApp.view_book")
        return True

    def has_object_permission(self, request: Request, view, obj: Book) -> bool:
        if view.action in ["retrieve", "update", "partial_update", "destroy"]:
            if request.user.has_perm("auth.permissionus.administrator"):
                return True
            # If the user is not an administrator, must own the book
            return obj.user == request.user and request.user.has_perm("BooksApp.view_book")
        return True
