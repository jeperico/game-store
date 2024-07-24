from apps.management import api
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(
    r"register-player",
    api.PlayerRegister,
    basename="register-player"
)
router.register(
    r"games",
    api.GamesViews
)
router.register(
    r"genres",
    api.GenresViews
)
router.register(
    r"categories",
    api.CategoriesViews
)

urlpatterns = [
    path("", include(router.urls)),
]