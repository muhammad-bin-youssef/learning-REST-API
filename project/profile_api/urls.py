from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HelloApiView, HelloViewSet
from profile_api import views

router = DefaultRouter()
router.register("vs", HelloViewSet, base_name="hello-viewset")
router.register("profile", views.UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", HelloApiView.as_view()),
]
