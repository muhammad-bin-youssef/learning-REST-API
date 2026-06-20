from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.viewsets import ViewSet

from .serializers import HelloSerializer


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


class HelloViewSet(ViewSet):
    serializer_class = HelloSerializer

    def list(self, request):
        return Response({"message": "hello"})

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}!"
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        return Response({"http_method": "GET"})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({"http_method": "PUT"})

    def partial_update(self, request, pk=None):

        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk=None):

        return Response({"http_method": "DELETE"})
