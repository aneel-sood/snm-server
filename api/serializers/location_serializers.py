from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import Location

class LocationSerializer(GeoFeatureModelSerializer):
  class Meta:
    model = Location
    geo_field = "lng_lat"
    fields = ('id', 'address')

  def create(self, validated_data):
    return Location.objects.create(**validated_data)

  def update(self, instance, validated_data):
    instance.address = validated_data.get('address', instance.address)
    instance.lng_lat = validated_data.get('lng_lat', instance.lng_lat)
    instance.save()
    return instance