from django.urls import path

from main import views

urlpatterns = [
    path(
        "users/todos",
        views.TodosView.as_view(),
    ),
    path(
        "users/manage",
        views.UsersManageView.as_view(),
    ),
    path(
        "user/todos",
        views.UserTodosView.as_view(),
    ),
    path(
        "user/todo",
        views.UserTodoView.as_view(),
    ),
    path(
        "user/todos/isfinished",
        views.UserTodosSortView.as_view(),
    ),
    path(
        "user/todo/manage/",
        views.UserManageView.as_view(),
    ),
]
# "user/todos/isfinished" -> I can just merge it with "user/todos" using just some logic
