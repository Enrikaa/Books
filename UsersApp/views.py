from django.contrib.auth.models import Permission
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from BooksApp.models import Book
from UsersApp.models import User
from UsersApp.serializers import PermissionSerializer, UserLoginSerializer
from UsersApp.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_scope = "users_list"

    @extend_schema(
        description="Creates user. Creating a user with administrator permission is not allowed through this endpoint."
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        super().create(request, *args, **kwargs)
        """Create a new user.

        Returns an empty list after successfully creating a user. The details of the created object are not immediately
        needed by the requirements.
        """
        return Response(data=[], status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserPermissionsView(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    This viewset provides an API endpoint to retrieve all available permissions.
    It can be used when creating a user to know the permission IDs before associating them with the user.
    """
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    throttle_scope = "permissions_list"

    def get(self, request: Request) -> Response:
        permissions = Permission.objects.all()
        permission_names = permissions.values_list("name", flat=True)
        serializer = PermissionSerializer(permission_names, many=True)
        return Response(serializer.data)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    queryset = Book.objects.all()
    throttle_scope = "login_list"

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data["access_token"]
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
