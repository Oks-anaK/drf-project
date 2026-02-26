from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import (CustomTokenObtainPairView, PaymentViewSet,
                         UserCreateAPIView, UserDestroyAPIView,
                         UserRetrieveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="user_destroy"),
]

urlpatterns += router.urls
