from rest_framework import serializers
from api.models import Resource

class ResourceSerializer(serializers.ModelSerializer):
  class Meta:
      model = Resource
      fields = ('id', 'type', 'details')