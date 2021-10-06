from django.db import models
from django.utils import timezone


class DataClass(models.Model):
	rep_dt = models.DateTimeField()
	delta = models.FloatField()
