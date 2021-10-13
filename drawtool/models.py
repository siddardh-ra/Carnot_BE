from django.db import models
from datetime import datetime
# Create your models here.
measures = (
    ('line', 'line'),
    ('poly', 'poly'),
    ('point', 'point'),
)


class AOI(models.Model):
    project = models.CharField(max_length=255, unique=True)
    label = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")
    creation_date=models.DateTimeField(default=datetime.now())
    polygon = models.TextField(default={}, null=True, blank=True)

    def __str__(self):
        return self.label + "_" + self.project


class Measure(models.Model):
    project = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=measures, default='')
    label = models.CharField(max_length=255, default="")
    description = models.CharField(max_length=255, default="")
    creation_date=models.DateTimeField(default=datetime.now())
    measurements = models.CharField(max_length=255,default="")
    polygon = models.TextField(default={}, null=True, blank=True)

    def __str__(self):
        return self.label + "_" + self.project
