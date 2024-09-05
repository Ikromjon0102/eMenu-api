from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from .views import index

schema_view = get_schema_view(
   openapi.Info(
      title="Foodme auth API",
      default_version='v1',
      description="Foodme uchun auth api v1.0",
      contact=openapi.Contact(email="ikromjon@gmail.com"),
      license=openapi.License(name="Demo License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('product/', include('product.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)