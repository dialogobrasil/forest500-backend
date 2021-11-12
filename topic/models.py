from django.db import models
from twitter.models import Status

class Topic(models.Model):
    name = models.TextField(primary_key=True)
    query = models.TextField()
    status = models.ManyToManyField(Status)