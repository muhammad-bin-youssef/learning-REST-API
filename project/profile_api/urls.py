from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HelloApiView, HelloViewSet

router = DefaultRouter()
router.register("vs", HelloViewSet, base_name="hello-viewset")

urlpatterns = [
    path("", include(router.urls)),
    path("", HelloApiView.as_view()),
]
