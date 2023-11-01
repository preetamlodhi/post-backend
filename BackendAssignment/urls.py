
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/', include('api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/token/verify/', TokenVerifyView.as_view(), name="verify_token"),
]
