from rest_framework import serializers
from api.models import Provider, Resource, Client, Need

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
      model = Resource
      fields = ('id', 'type', 'details')

class ProviderSerializer(serializers.ModelSerializer):
  resources = ResourceSerializer(many=True)
  class Meta:
    model = Provider
    fields = ('id', 'first_name', 'last_name', 'email', 'resources')

class NeedSerializer(serializers.ModelSerializer):
  class Meta:
      model = Need
      fields = ('id', 'type', 'requirements', 'status')

class ClientSerializer(serializers.ModelSerializer):
  needs = NeedSerializer(many=True)
  class Meta:
    model = Client
    fields = ('id', 'first_name', 'last_name', 'email', 'needs')

class DashboardClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = (
      'id', 'first_name', 'last_name', 'fulfilled_needs_count', 
      'pending_needs_count', 'latest_resource_bookmark_datetime'
    )