from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from UsersApp.examples import USER_CREATION_PAYLOAD, USER_LOGIN_PAYLOAD
from UsersApp.models import User
from UsersApp.type_hints import UserCreationDict
from utils import Errors


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User create example",
            value=USER_CREATION_PAYLOAD,
            request_only=True,
        ),
    ]
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "user_permissions"]

    def create(self, validated_data: UserCreationDict) -> UserCreationDict:
        user_permissions = validated_data.get("user_permissions", [])
        administrator_permission = Permission.objects.get(codename="administrator")

        if administrator_permission in user_permissions:
            raise ValidationError({"user_permissions": Errors.CANNOT_CREATE_A_USER})

        return super().create(validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Added custom MyTokenObtainPairSerializer for additional fields in token payload."""
    @classmethod
    def get_token(cls, user: User) -> str:
        token_data = super().get_token(user)
        token_data["username"] = user.username
        return token_data


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        exclude = ["content_type", "codename"]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User login example",
            value=USER_LOGIN_PAYLOAD,
            request_only=True,
        ),
    ]
)
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        attrs["access_token"] = str(refresh.access_token)
        return attrs
