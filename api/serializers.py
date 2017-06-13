from rest_framework import serializers
from api.models import Provider, Resource, Client, Need, NeedResourceMatch

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
      fields = ('id', 'type', 'requirements')

class ResourceMatchStatusSerializer(serializers.ModelSerializer):
  resource = ResourceSerializer()
  class Meta: 
    model = NeedResourceMatch
    fields = ('pending', 'fulfilled', 'resource')

class NeedResourceMatchStatusSerializer(serializers.ModelSerializer):
  resources = ResourceMatchStatusSerializer(source='needresourcematch_set', many=True)
  class Meta:
      model = Need
      fields = ('id', 'type', 'requirements', 'resources')

class ClientSerializer(serializers.ModelSerializer):
  needs = NeedResourceMatchStatusSerializer(many=True)
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