from django.db import models

class Resource(models.Model):
  type = models.CharField(max_length=50)