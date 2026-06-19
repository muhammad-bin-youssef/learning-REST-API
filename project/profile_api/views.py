from rest_framework.response import Response
from rest_framework.views import APIView, status

from .serializers import EchoSerializer, HelloSerializer


class HelloApiView(APIView):
    serializer_class = HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
            "H1",
        ]
        return Response({"message": "hello", "an_apiview": an_apiview})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"
            return Response({"message": message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({"message": "PUT"})

    def patch(self, request, pk=None):
        return Response({"message": "PATCH"})

    def delete(self, request, pk=None):
        return Response({"message": "DELETE"})


class EchoView(APIView):
    serializer_class = EchoSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response({"message": serializer.validated_data.get("name")})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
