from django.db import models
from django.conf import settings


class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateField()
    time = models.DurationField()
    distance = models.FloatField()
