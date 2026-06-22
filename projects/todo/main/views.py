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


class TodoCreateView(APIView):
    serializer_class = serializers.CreateTodo

    def post(self, request):
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


class UserManageView(APIView):
    serializer_class = serializers.CreateUser

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
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
