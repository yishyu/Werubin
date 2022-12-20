"""werubin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

# swagger import
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from werubin.generators import BothHttpAndHttpsSchemaGenerator


api_urlpatterns = [
    path('', include(('feeds.urls', 'feeds'), namespace='feeds')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
schema_view = get_schema_view(
    openapi.Info(
        title="WERUBIN API Documentation",
        default_version='v1',
        description="🙌 READ ME !!! 🙌 \n In this swagger, you will find all the api endpoint that we provide you. \n\
        This api allows you to interact in any way (except to registering process) with the content of our website \
        in case you want to build an app on top of ours.\
        Note that in order to user the api, you need to be registered on our website. \n \
        We are using Basic Authentication so you can either add the authorization header with your username and password encoded in Base64 separated by a column (:) \
        or if you are using curl, the -u option should work just fine.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    patterns=api_urlpatterns,
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.IsAuthenticated],
)
urlpatterns = api_urlpatterns + [

    path('travels/', include(('travels.urls', 'travels'), namespace='travels')),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path('admin/', admin.site.urls),
    # json and yaml version
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # 2 different UI of swagger
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # background image in css file
    path('css/users.css', TemplateView.as_view(
        template_name='users.css',
        content_type='text/css')
    ),
    path('js/addToAlbumModal.js', TemplateView.as_view(
        template_name='addToAlbumModal.js',
        content_type='text/javascript')
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
