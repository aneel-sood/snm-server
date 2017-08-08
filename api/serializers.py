from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Provider, Resource, Client, Need, NeedResourceMatch, Location

class LocatinSerializer(GeoFeatureModelSerializer):
  class Meta:
      model = Location
      geo_field = "lng_lat"
      fields = ('id', 'city')

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
      model = Resource
      fields = ('id', 'type', 'details')

class ProviderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Provider
    fields = ('id', 'first_name', 'last_name', 'email')

class ProviderWithResourcesSerializer(serializers.ModelSerializer):
  resources = ResourceSerializer(many=True)
  class Meta:
    model = Provider
    fields = ('id', 'first_name', 'last_name', 'email', 'resources')

class ResourceWithProviderSerializer(serializers.ModelSerializer):
  provider = ProviderSerializer()
  class Meta:
    model = Resource
    fields = ('id', 'type', 'details', 'provider')

class NeedSerializer(serializers.ModelSerializer):
  class Meta:
      model = Need
      fields = ('id', 'type', 'requirements')

class ResourceMatchStatusSerializer(serializers.ModelSerializer):
  resource = ResourceWithProviderSerializer()
  class Meta: 
    model = NeedResourceMatch
    fields = ('pending', 'fulfilled', 'resource')

class NeedResourceMatchStatusSerializer(serializers.ModelSerializer):
  resources = ResourceMatchStatusSerializer(source='needresourcematch_set', many=True)
  class Meta:
      model = Need
      fields = ('id', 'type', 'requirements', 'created_at', 'resources')

class ClientSerializer(serializers.ModelSerializer):
  needs = NeedResourceMatchStatusSerializer(many=True)
  location = LocatinSerializer()
  class Meta:
    model = Client
    fields = ('id', 'first_name', 'last_name', 'email', 'needs', 'location')

class DashboardClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = (
      'id', 'first_name', 'last_name', 'needs_without_matching_resources_count',
      'needs_with_matching_resources_count', 'pending_needs_count', 
      'fulfilled_needs_count', 'most_recent_match_activity_datetime'
    )