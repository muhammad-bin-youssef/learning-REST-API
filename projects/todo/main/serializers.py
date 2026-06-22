from rest_framework import serializers


class UserTodos(serializers.Serializer):
    username = serializers.CharField(max_length=255)


class UserTodo(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    note_title = serializers.CharField(max_length=255)


class UserTodosSort(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    is_finished = serializers.BooleanField(default=False, required=False)


class CreateTodo(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    note_title = serializers.CharField(max_length=255)
    note = serializers.CharField(max_length=2048, required=False, default="")
    is_finished = serializers.BooleanField(default=False, required=False)


class CreateUser(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
