from rest_framework import serializers
from api.models import Provider, Resource

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
      model = Resource
      fields = ('id', 'type', 'details')

class ProviderSerializer(serializers.ModelSerializer):
  resources = ResourceSerializer(many=True)
  class Meta:
    model = Provider
    fields = ('id', 'first_name', 'last_name', 'email', 'resources')