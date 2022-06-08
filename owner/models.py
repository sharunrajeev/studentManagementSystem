from django.db import models


# Create your models here.
class Applicants(models.Model):
    Name = models.CharField(max_length=100, default=None)
    Age = models.IntegerField(default=None)
    Gender = models.CharField(max_length=12, default=None)
    Address = models.CharField(max_length=100, default=None)
    Email = models.EmailField(max_length=100, default=None)
    Department = models.CharField(max_length=100, default=None)
    Eligibility = models.BooleanField(blank=True, null=True, default=None)


class Candidates(models.Model):
    ApplicationId = models.ForeignKey(Applicants, on_delete=models.CASCADE, default=False)
    UserId = models.CharField(max_length=100)
    Photo = models.ImageField(upload_to='pics')
    Achievements = models.TextField()
    PaymentStatus = models.BooleanField(default=False)
    Marks = models.IntegerField(blank=True, null=True, default=None)
    Attendance = models.IntegerField(blank=True, null=True, default=None)
