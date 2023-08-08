import jwt
from django.conf import settings
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from utils import BaseTestCase, Errors


class UsersTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user_data = {"email": "enrika1@gmail.com",
                          "username": "test1",
                          "password": "tes",
                          "is_staff": True
                          }
        self.administrator_permission = Permission.objects.get(codename="administrator")

    def test_can_create_user(self):
        response = self.client.post(reverse("users-list"), data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_cannot_create_user_with_administrator_permission_through_the_endpoint(self):
        self.user_data["user_permissions"] = [self.administrator_permission.id, ]
        response = self.client.post(reverse("users-list"), data=self.user_data)
        self.assertEqual(response.data["user_permissions"], Errors.CANNOT_CREATE_A_USER.value)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successfully_create_user_with_administrator_permission_through_the_admin(self):
        self.user_data["user_permissions"] = [self.administrator_permission.id, ]
        response = self.client.post(reverse("users-list"), data=self.user_data)
        self.assertEqual(response.data["user_permissions"], Errors.CANNOT_CREATE_A_USER.value)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_permissions(self):
        response = self.client.get(reverse("user-permissions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 37)


class JwtTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login_data = {
            "username": self.username,
            "password": self.password,
        }

    def test_rotate_refresh_token(self):
        """Checking if a new refresh token will be returned along with the new access token"""
        black_listed_token = BlacklistedToken.objects.first()
        self.assertIsNone(OutstandingToken.objects.first())
        self.assertIsNone(black_listed_token)
        response = self.client.post(reverse("token_obtain_pair"), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_token(self):
        """
        Test obtaining an access token and accessing a protected API endpoint.

        The test authenticates the user using their credentials to obtain an access token.
        It then uses the access token to make an authenticated GET request to the "users-list"
        API endpoint and verifies the response contains the user's information.
        """
        response = self.client.post(reverse("token_obtain_pair"), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        access_token = response.data["access"]
        auth_header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.get(reverse("users-list"), **auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_refresh_token(self):
        """
        Test refreshing an access token using a refresh token.

        The test authenticates the user using their credentials to obtain an access token.
        It then uses the access token to obtain a refresh token. The refresh token is
        then used to request a new access token. The test verifies that the new access token
        is different from the initial one, and it uses the new access token to make an
        authenticated GET request to the "users-list" API endpoint, ensuring the response
        contains the user's information.
        """
        response = self.client.post(reverse("token_obtain_pair"), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(reverse("token_refresh"), data=refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        new_access_token = response.data["access"]
        self.assertNotEqual(access_token, new_access_token)
        auth_header = {"HTTP_AUTHORIZATION": f"Bearer {new_access_token}"}
        response = self.client.get(reverse("users-list"), **auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_token_blacklisting_on_expiry(self):
        """
        When a user logs in and receives a token, the token should include custom fields (username and email) in its
        payload, as correctly implemented in the custom serializer. However, please note that the "OutstandingToken"
        model in the database is not responsible for storing custom fields. Therefore, it is important to highlight that
        when blacklisting tokens, OutstandingToken should not be filtered based on access/refresh tokens, as it does not
        contain the custom fields.

        Note: The test will also check that refresh tokens submitted to the TokenRefreshView will be added to the
        blacklist app.
        """
        self.assertIsNone(OutstandingToken.objects.first())
        self.assertIsNone(BlacklistedToken.objects.first())
        response = self.client.post(reverse("token_obtain_pair"), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]
        outstanding_token = OutstandingToken.objects.first()
        self.assertIsNotNone(outstanding_token.token)
        auth_header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        users_list_response = self.client.get(reverse("users-list"), **auth_header)
        self.assertEqual(users_list_response.status_code, status.HTTP_200_OK)
        BlacklistedToken.objects.create(token=outstanding_token)
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(reverse("token_refresh"), data=refresh_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], Errors.TOKEN_IS_BLACKLISTED.value)

    def test_jwt_token_custom_payload_fields(self):
        response = self.client.post(reverse("token_obtain_pair"), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]
        decoded_access_token_payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        decoded_refresh_token_payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        self.assertEqual(decoded_access_token_payload["username"], self.user.username)
        self.assertEqual(decoded_refresh_token_payload["username"], self.user.username)


class ThrottlingTestCase(BaseTestCase):
    def test_reach_throttling_in_users_list_api(self):
        login_data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(reverse("token_obtain_pair"), data=login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        access_token = response.data["access"]
        auth_header = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.get(reverse("users-list"), **auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(settings.API_THROTTLE_ENABLED)
        max_throttle_count = int(settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["users_list"][:2])
        for i in range(0, max_throttle_count - 1):
            response = self.client.get(reverse("users-list"), **auth_header)
            self.assertEqual(response.status_code, status.HTTP_200_OK,
                             f"Failed after {i} calls. {response.content}")
        response = self.client.get(reverse("users-list"), **auth_header)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS, response.content)
