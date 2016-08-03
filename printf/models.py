from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Customers(models.Model):
    name=models.CharField(max_length=30)
    user = models.ForeignKey(User)
    location = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class Merchants(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    cost=models.PositiveIntegerField(validators=[MinValueValidator(5)])
    def __unicode__(self):
        return self.name

class Orders(models.Model):
    qty=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    date_of_order=models.DateField()
    date_of_delivery=models.DateField()
    customer = models.ForeignKey(Customers)
    merchant = models.ForeignKey(Merchants)
    completed=models.BooleanField(default=False)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def __unicode__(self):
        return self.customer.name
