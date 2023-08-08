from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from BooksApp.views import BookViewSet
from UsersApp.views import UserViewSet, MyTokenObtainPairView, UserPermissionsView, UserLoginView

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("books", BookViewSet, basename="books")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/user/permissions/', UserPermissionsView.as_view({"get": "list"}), name="user-permissions"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
]
