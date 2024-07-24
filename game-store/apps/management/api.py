from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from utils.actions import DRFAction
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from rest_framework.response import Response
from rest_framework import (
    generics,
    mixins,
    permissions,
    response,
    status,
    views,
    viewsets,
    filters,
)
from .models import Games, User, Player, Category, Genre
from .serializers import (
    UserReadOnlySerializer,
    UserRegisterSerializer,
    UserChangePasswordSerializer,
    UserReadOnlySerializer,
    ProfileTokenObtainPairSerializer,
    PlayerRegisterSerializer,
    GamesSerializer,
    GenresSerializer,
    CategoriesSerializer,
)

class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserReadOnlySerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]

    def get_serializer_class(self):
        return (
            self.serializer_class
            if DRFAction.is_list(self.action)
            else UserReadOnlySerializer
        )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        serializer = UserReadOnlySerializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserRegister(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.none()

    def perform_create(self, serializer):
        res = super().perform_create(serializer)
        return res


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BlacklistedToken.objects.none()
    serializer_class = None

    def post(self, request):
        tokens = OutstandingToken.objects.filter(id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return response.Response(status=status.HTTP_205_RESET_CONTENT)


class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserChangePasswordSerializer


class ProfileTokenObtainPairView(TokenObtainPairView):
    serializer_class = ProfileTokenObtainPairSerializer

# Create your views here.
class PlayerRegister(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = PlayerRegisterSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Player.objects.none()

    def perform_create(self, serializer):
        res = super().perform_create(serializer)
        return res


class GamesViews(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer


class GenresViews(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class CategoriesViews(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
