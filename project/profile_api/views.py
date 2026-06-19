from rest_framework.response import Response
from rest_framework.views import APIView


class HelloApiView(APIView):
    def get(self, request, format=None):
        an_apiview = [
            "H1",
        ]
        return Response({"message": "hello", "an_apiview": an_apiview})
