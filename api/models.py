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
