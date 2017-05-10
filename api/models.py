from django.db import models
from django.contrib.postgres.fields import JSONField

class Resource(models.Model):
  type = models.CharField(max_length=50)
  details = JSONField(default=dict)