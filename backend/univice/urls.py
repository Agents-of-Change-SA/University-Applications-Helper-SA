from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Univice API",
        default_version='v1',
        description="Backend API for the Univice mobile application",
        contact=openapi.Contact(email="gxagxakatleho@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/', include('profiles.urls')),
    path('api/', include('school.urls')),
    path('api/', include('careers.urls')),
    path('api/', include('qualifications.urls')),
    path('api/', include('tutors.urls')),
    path('api/', include('applications.urls')),
    # Docs — under api/ prefix
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
