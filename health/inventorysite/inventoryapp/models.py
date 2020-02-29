from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone


# Create your models here.


class Lender(models.Model):
    lender = models.CharField(max_length=200)
    image = models.FileField(null=True,blank=True)
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=500)
    department=models.CharField(max_length=100,default="")
    safety_deposit= models.IntegerField()
    contact_number= models.IntegerField()
    availability=models.BooleanField(default=True)
    def __str__(self):
        return self.product_name

  

class Borrower(models.Model):
    borrower = models.CharField(max_length=200)
    sap_id = models.IntegerField()
    email = models.CharField(max_length=100)
    product_name=models.CharField(max_length=200)
    def __str__(self):
        return self.borrower









  


