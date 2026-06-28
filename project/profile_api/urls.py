from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HelloApiView, HelloViewSet
from profile_api import views

router = DefaultRouter()
router.register("", HelloViewSet, base_name="hello-viewset")
router.register("profile", views.UserProfileViewSet)
router.register("feed", views.UserProfileFeedViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("hello", HelloApiView.as_view()),
    path(
        "log",
        views.UserLoginApiView.as_view(),  # api/log
    ),
]
