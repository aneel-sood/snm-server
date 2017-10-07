from rest_framework import serializers
from api.models import Provider, Resource, Need, NeedResourceMatch
from .location_serializers import LocationSerializer

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Resource
    fields = ('id', 'type', 'details')

class ProviderSerializer(serializers.ModelSerializer):
  location = LocationSerializer(allow_null=True)
  
  class Meta:
    model = Provider
    fields = ('id', 'first_name', 'last_name', 'referrer', 
      'email', 'cell_phone', 'home_phone', 'location')

  def create(self, validated_data):
    location = self.crupdate_location(validated_data.pop('location'))    

    return Provider.objects.create(**validated_data, location=location)

  def update(self, instance, validated_data):
    location = self.crupdate_location(validated_data.pop('location'), instance.location)    
 
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.referrer = validated_data.get('referrer', instance.referrer)
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

class ResourceWithProviderSerializer(serializers.ModelSerializer):
  provider = ProviderSerializer()
  class Meta:
    model = Resource
    fields = ('id', 'type', 'details', 'provider')

class ProviderWithResourcesSerializer(serializers.ModelSerializer):
  resources = ResourceSerializer(many=True)
  class Meta:
    model = Provider
    fields = ('id', 'first_name', 'last_name', 'email', 'resources')

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
