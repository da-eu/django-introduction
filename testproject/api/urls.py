from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from .views import CommentViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

info = openapi.Info(
    title='Forum API',
    default_version='v1',
    description='掲示板アプリ向けAPI',
    contact=openapi.Contact(email='daeu@test.com'),
    license=openapi.License(name="Apache 2.0", url="http://www.apache.org/licenses/LICENSE-2.0.html"),
)

schema_view = get_schema_view(
    info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('token/', obtain_auth_token)
]