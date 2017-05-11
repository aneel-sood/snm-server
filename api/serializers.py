from rest_framework import serializers
from api.models import Provider, Resource

class ProviderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Provider
    fields = ('first_name', 'last_name', 'email')

class ResourceSerializer(serializers.ModelSerializer):
  provider = ProviderSerializer(read_only='True')
  class Meta:
      model = Resource
      fields = ('id', 'type', 'details', 'provider')