from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import Count

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
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def fulfilled_needs_count(self):
    return self.needs.filter(needresourcematch__fulfilled = True).count()

  def pending_needs_count(self):
    return self.needs.exclude(needresourcematch__fulfilled = True).count()

  def latest_resource_bookmark_datetime(self):
    needs_with_bookmarked_resoureces = self.needs.annotate(num_resources=Count('resources')).exclude(num_resources = 0)
    if needs_with_bookmarked_resoureces:
      need_with_latest_bookmark = needs_with_bookmarked_resoureces.latest('needresourcematch__updated_at')
      return need_with_latest_bookmark.needresourcematch_set.latest('updated_at').updated_at
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
