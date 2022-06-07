from django.db import models

# Create your models here.

class Applicants(models.Model):
    Name = models.CharField(max_length=100, default=None)
    Age = models.IntegerField(default=None)
    Gender= models.CharField(max_length=12, default=None)
    Address = models.CharField(max_length=100, default=None)
    Email = models.EmailField(max_length=100, default=None)
    Department= models.CharField(max_length=100, default=None)
    Eligibility= models.BooleanField(default=False)





