from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)


class EchoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
