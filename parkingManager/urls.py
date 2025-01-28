from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("parking.urls"), name="parking.urls"),
    path(
        "api/login",
        TokenObtainPairView.as_view(),
    ),
    path(
        "api/token/refresh",
        TokenObtainPairView.as_view(),
    ),
]
