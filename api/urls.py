from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

# Create a router and register the viewsets with it.
router = DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"users", views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("latestusers/", views.LatestUserView.as_view(), name="latestusers"),
]
