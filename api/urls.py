from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

app_name = "api"

router = DefaultRouter()
router.register("users", UsersViewSet, basename="users")


schema_view = get_schema_view(
    openapi.Info(
        title="API Referal system",
        default_version="v1",
        description="API documentation for Referal system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourdomain.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc-schema"
    ),
    path("", include(router.urls)),
]
