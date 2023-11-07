from django.contrib.auth import authenticate
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone
from datetime import timedelta
from api.models import Post, User
from api.permissions import IsOwnerOrReadOnly, IsABCUser
from api.renderers import UserRenderer
from api.serializers import (
    PostSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {"token": token, "message": "Registration Successful"},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "message": "Login Success"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"errors": {"field_errors": ["Email or Password is not Valid"]}},
                status=status.HTTP_404_NOT_FOUND,
            )


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update`
    and `destroy` actions.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

class LatestUserView(APIView):
    permission_classes = [IsABCUser, permissions.IsAuthenticated]

    def get(self, request, format=None):
        queryset = User.objects.filter(created_at__gte=timezone.now()-timedelta(days=1))
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
