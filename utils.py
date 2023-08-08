from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework.test import APIClient

from UsersApp.enums import ChoicesEnum
from UsersApp.models import User


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.email = "admin@admin.com"
        self.username = "testusername"
        self.password = "admin"
        self.re_password = "testpassword"
        self.is_staff = True
        self.user = User.objects.create_user(email=self.email, username=self.username, password=self.password,
                                             is_staff=self.is_staff
                                             )
        self.user2 = User.objects.create_user(email='user2@gmail.com', username='user2', password=self.password,
                                              is_staff=self.is_staff
                                              )
        permissions = Permission.objects.filter(codename__in=['add_book', 'delete_book', 'change_book', 'view_book'])
        self.user.user_permissions.add(*permissions)
        self.client.force_authenticate(self.user)


class StringChoicesEnum(str, ChoicesEnum):
    pass


class Errors(StringChoicesEnum):
    """
    Created a separate errors class to handle all errors in one place.
    Error messages use underscores for easier error catching on the frontend and and, if necessary, renaming without
    breaking the system.
    """
    CANNOT_CREATE_A_USER = "error_cannot_create_a_user_with_administrator_permission."
    TOKEN_IS_BLACKLISTED = "Token is blacklisted"
    PERMISSION_DENIED = "You do not have permission to perform this action."
