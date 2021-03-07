from django.db import models

# Create your models here.
class Tracker(models.Model):
    name = models.CharField(max_length = 20)
    date = models.DateField()
    weight = models.IntegerField()
