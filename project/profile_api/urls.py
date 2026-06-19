from django.urls import path

from .views import EchoView, HelloApiView

urlpatterns = [
    path("", HelloApiView.as_view()),
    path("echo/", EchoView.as_view()),
]
