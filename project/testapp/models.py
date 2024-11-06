from django.db import models
from django.contrib.auth.models import User


class Adviser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=50)


class Machine(models.Model):
    name = models.CharField(max_length=50)
    spares = models.ManyToManyField(Spare)
