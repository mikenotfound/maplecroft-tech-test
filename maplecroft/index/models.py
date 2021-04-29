from django.db import models

class Index(models.Model):
    name = models.CharField(max_length=255)

class IndexVersion(models.Model):
    index = models.ForeignKey(Index, on_delete=models.CASCADE)
    version = models.IntegerField()
    score = models.FloatField()
    timestamp = models.DateTimeField()