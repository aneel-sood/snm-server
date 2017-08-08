from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import Count

class Location(models.Model):
  address = models.CharField(max_length=60)
  city = models.CharField(max_length=30)
  province = models.CharField(max_length=30)
  postal_code = models.CharField(max_length=30)
  lng_lat = models.PointField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Provider(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=60)
  email = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Resource(models.Model):
  type = models.CharField(max_length=50)
  details = JSONField(default=dict)
  provider = models.ForeignKey(Provider, related_name='resources', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Client(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=60)
  email = models.CharField(max_length=100)
  location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def needs_without_matching_resources_count(self):
    return self.needs.annotate(num_resources=Count('resources')).exclude(num_resources__gt = 0).count()

  def needs_with_matching_resources_count(self):
    return self.needs.filter(needresourcematch__fulfilled = False, needresourcematch__pending = False).count()

  def pending_needs_count(self):
    return self.needs.filter(needresourcematch__pending = True).count()

  def fulfilled_needs_count(self):
    return self.needs.filter(needresourcematch__fulfilled = True).count()

  def most_recent_match_activity_datetime(self):
    needs_with_matched_resources = self.needs.annotate(num_resources=Count('resources')).exclude(num_resources = 0)
    if needs_with_matched_resources:
      need_with_most_recent_match_activity = needs_with_matched_resources.latest('needresourcematch__updated_at')
      return need_with_most_recent_match_activity.needresourcematch_set.latest('updated_at').updated_at
    else:
      return None

class Need(models.Model):
  type = models.CharField(max_length=50)
  requirements = JSONField(default=dict)
  client = models.ForeignKey(Client, related_name='needs', on_delete=models.CASCADE)
  resources = models.ManyToManyField(Resource, through='NeedResourceMatch')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class NeedResourceMatch(models.Model):
  need = models.ForeignKey(Need, on_delete=models.CASCADE)
  resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
  fulfilled = models.BooleanField(default=False)
  pending = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
