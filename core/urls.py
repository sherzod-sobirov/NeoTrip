from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from order.call_back import PaymeCallBackAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from main.views import *
from order.views import GeneratePayLinkAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="Neo Trip Tour API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contactsardor@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('payments/merchant/', PaymeCallBackAPIView.as_view(), name='payme_callback'),
    path('pay-link/', GeneratePayLinkAPIView.as_view(), name='generate-pay-link')
]

urlpatterns += i18n_patterns(
    path("",include("user.urls")),
    path("",include("main.urls")),
    path("",include("tour.urls")),
    path("", include('post.urls')),
    path("", include('order.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('set-language/', set_language, name='set_language'),
)

urlpatterns += i18n_patterns(
    path('', include('main.urls')),  # Your app's URLs
    # Add other URLs for your app as necessary
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
