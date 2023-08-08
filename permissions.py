
from django.utils.dateformat import format as datetime_format
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from UsersApp.models import User





class CustomPermissionIsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        token = RefreshToken.for_user(request.user)
        print(token, "ALIOOOOOOO")
        return bool(request.user and request.user.is_authenticated)
