from rest_framework import serializers
from api.models import Client, Need
from .location_serializers import LocationSerializer
from .provider_serializers import NeedResourceMatchStatusSerializer
import re

class NeedSerializer(serializers.ModelSerializer):
  class Meta:
      model = Need
      fields = ('id', 'type', 'requirements')

class NeedCSVSerializer(serializers.ModelSerializer):
  requirements = serializers.CharField()
  created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

  class Meta:
    model = Need
    fields = ('client_id', 'type', 'requirements', 'created_at', 'matching_resources_count',
                'pending_resources_count', 'fulfilled_resources_count')

  def to_representation(self, instance):
    representation = super(NeedCSVSerializer, self).to_representation(instance)
    representation['requirements'] = re.sub('[{}]', '', representation['requirements'])
    return representation

class ClientCSVSerializer(serializers.ModelSerializer):
  location = serializers.SlugRelatedField(slug_field='address', read_only=True)
  most_recent_match_activity_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

  class Meta:
    model = Client
    fields = ('id', 'first_name', 'last_name', 'birthdate', 
      'email', 'cell_phone', 'home_phone', 'location', 
      'needs_without_matching_resources_count',
      'needs_with_matching_resources_count', 'pending_needs_count', 
      'fulfilled_needs_count', 'most_recent_match_activity_datetime')

class ClientSerializer(serializers.ModelSerializer):
  location = LocationSerializer(allow_null=True)
  needs = NeedResourceMatchStatusSerializer(many=True, read_only=True)
  
  class Meta:
    model = Client
    fields = ('id', 'first_name', 'last_name', 'birthdate', 
      'email', 'cell_phone', 'home_phone', 'needs', 'location')

  def create(self, validated_data):
    location = self.crupdate_location(validated_data.pop('location'))    

    return Client.objects.create(**validated_data, location=location)

  def update(self, instance, validated_data):
    location = self.crupdate_location(validated_data.pop('location'), instance.location)    
 
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.birthdate = validated_data.get('birthdate', instance.birthdate)
    instance.email = validated_data.get('email', instance.email)
    instance.cell_phone = validated_data.get('cell_phone', instance.cell_phone)
    instance.home_phone = validated_data.get('home_phone', instance.home_phone)
    instance.location = location
    instance.save()
    
    return instance

  def crupdate_location(self, data, instance=None):
    if data is None:
      if instance: instance.delete() 
      location = None
    else:
      location_serializer = LocationSerializer(instance, data=data) if instance else LocationSerializer(data=data)
      if location_serializer.is_valid(): location = location_serializer.save() 

    return location

class DashboardClientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Client
    fields = (
      'id', 'first_name', 'last_name', 'needs_without_matching_resources_count',
      'needs_with_matching_resources_count', 'pending_needs_count', 
      'fulfilled_needs_count', 'most_recent_match_activity_datetime'
    )