from django.db import models


class Employee(models.Model):
    no = models.IntegerField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.FloatField()
    address = models.CharField(max_length=50)

