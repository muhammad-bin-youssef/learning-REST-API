from django.urls import path

from .views import TodoView

urlpatterns = [
    path(
        "Todos",
        TodoView.as_view(),
    ),
]
