from django.db import models
from django.contrib.postgres.fields import JSONField

class Provider(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=60)
  email = models.CharField(max_length=100)

class Resource(models.Model):
  type = models.CharField(max_length=50)
  details = JSONField(default=dict)
  provider = models.ForeignKey(Provider, related_name='resources', on_delete=models.CASCADE)

class Client(models.Model):
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=60)
  email = models.CharField(max_length=100)

class Need(models.Model):
  type = models.CharField(max_length=50)
  requirements = JSONField(default=dict)
  status = models.CharField(max_length=20)
  client = models.ForeignKey(Client, related_name='needs', on_delete=models.CASCADE)
