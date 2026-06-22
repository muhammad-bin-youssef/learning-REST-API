from rest_framework import status
from rest_framework.test import APITestCase

from main import models


class TodoTests(APITestCase):
    def test_get_all_todos(self):
        response = self.client.get("/api/users/todos/")
        self.assertEqual(response.status_code, ...)

    def test_create_todo_success(self):
        response = self.client.post(
            "/api/user/todo/manage/",
            {
                "username": ...,
                "note_title": ...,
                "note": ...,
                "is_finished": ...,
            },
            format="json",
        )
        self.assertEqual(response.status_code, ...)
        self.assertEqual(response.data["note_title"], ...)

    def test_create_todo_user_not_found(self):
        response = self.client.post(
            "/api/user/todo/manage/",
            {
                "username": ...,
                "note_title": ...,
            },
            format="json",
        )
        self.assertEqual(response.status_code, ...)
