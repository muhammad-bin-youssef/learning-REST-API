from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .serializers import HelloSerializer
from profile_api import serializers
from profile_api import models
from profile_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


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


class HelloViewSet(viewsets.ViewSet):
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

        return Response({"ObtainAuthToken": "DELETE"})


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)
