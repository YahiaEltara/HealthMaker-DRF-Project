from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Schema generation endpoint
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/refresh-token/', TokenRefreshView.as_view()),

    path('api/', include('api.urls')),
    
]
