from posix import stat_result

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, status

from main import models, serializers


class TodosView(APIView):
    def get(self, request):
        todos = list(models.Task.objects.values())
        return Response({"todos": todos})


class UserTodosView(APIView):
    serializer_class = serializers.UserTodos

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            user = get_object_or_404(models.User, username=username)
            todos = list(user.tasks.values())
            return Response({"user": user.username, "todos": todos})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTodoView(APIView):
    serializer_class = serializers.UserTodo

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            user = get_object_or_404(models.User, username=username)
            note_title = serializer.validated_data.get("note_title")
            todo = user.tasks.filter(title=note_title).values()
            return Response({"user": user.username, "todo": todo})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTodosSortView(APIView):
    serializer_class = serializers.UserTodosSort

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            user = get_object_or_404(models.User, username=username)
            is_finished = serializer.validated_data.get("isfinished")
            todos = list(user.tasks.filter(is_finished=is_finished).values())
            return Response({"user": user.username, "todos": todos})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManageView(APIView):
    serializer_class = serializers.CreateTodo

    def post(self, request):
        """
        Create post
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            user = get_object_or_404(models.User, username=username)
            note_title = serializer.validated_data.get("note_title")
            note = serializer.validated_data.get("note")
            is_finished = serializer.validated_data.get("is_finished")
            todo = user.tasks.create(
                title=note_title, note=note, is_finished=is_finished
            )
            return Response(
                {
                    "user": user.username,
                    "note_id": todo.id,
                    "note_title": note_title,
                    "note": note,
                    "is_finished": is_finished,
                }
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        serializer = serializers.PatchTodo(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            old_todo_title = serializer.validated_data.get("old_todo_title")
            user = get_object_or_404(models.User, username=username)
            todo = get_object_or_404(user.tasks, title=old_todo_title)
            title = serializer.validated_data.get("new_todo_title")
            note = serializer.validated_data.get("note")
            is_finished = serializer.validated_data.get("new_is_finished")

            if title is None:
                title = todo.title

            if note is None:
                note = todo.note

            if is_finished is None:
                is_finished = todo.is_finished

            todo.title = title
            todo.note = note
            todo.is_finished = is_finished

            todo.save()

            return Response(
                {
                    "user": user.username,
                    "note_id": todo.id,
                    "note_title": title,
                    "note": note,
                    "is_finished": is_finished,
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            title = serializer.validated_data.get("title")
            user = get_object_or_404(models.User, username=username)
            todo = get_object_or_404(user.tasks, title=title)

            todo.delete()

            return Response(
                {
                    "username": username,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersManageView(APIView):
    serializer_class = serializers.CreateUser

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            check_user = models.User.objects.filter(username=username).exists()
            if check_user is None:
                return Response(
                    {"error": "Username already exist"}, status=status.HTTP_409_CONFLICT
                )
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = models.User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            return Response({"user": username, "user_id": user.id, "email": email})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        serializer = serializers.DeleteUser(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            user = get_object_or_404(models.User, username=username)
            password = serializer.validated_data.get("password")
            is_correct_password = user.check_password(password)
            if is_correct_password:
                user.delete()
                return Response(
                    {"message": f"User {username} deleted"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid password"}, status=status.HTTP_403_FORBIDDEN
                )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
