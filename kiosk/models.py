from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()


class Child(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()


class IceCream(models.Model):
    flavor = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class IceCreamKiosk(models.Model):
    location = models.CharField(max_length=100)
    ice_creams = models.ManyToManyField(IceCream)
