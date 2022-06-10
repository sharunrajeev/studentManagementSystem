from django.db import models


# Create your models here.
class Applicants(models.Model):
    Name = models.CharField(max_length=100, default=None)
    Age = models.IntegerField(default=None)
    Gender = models.CharField(max_length=12, default=None)
    Address = models.CharField(max_length=100, default=None)
    Mob = models.CharField(max_length=13, default=None)
    Email = models.EmailField(max_length=100, default=None)
    Department = models.CharField(max_length=100, default=None)
    University = models.CharField(max_length=100, default=None)
    Dob = models.DateField(default=None)
    Phd_Reg = models.IntegerField(default=None)
    Phd_Joining_Date = models.DateField(default=None)
    Research_Topic = models.CharField(max_length=100, default=None)
    Research_Guide = models.CharField(max_length=100, default=None)
    Guide_Mail = models.EmailField(max_length=100, default=None)
    Guide_Phone = models.CharField(max_length=13, default=None)
    Eligibility = models.BooleanField(blank=True, null=True, default=None)


class Candidates(models.Model):
    ApplicationId = models.ForeignKey(Applicants, on_delete=models.CASCADE, default=False)
    UserId = models.CharField(max_length=100)
    Photo = models.ImageField(upload_to='pics')
    Achievements = models.TextField()
    PaymentStatus = models.BooleanField(default=False)
    Marks = models.IntegerField(blank=True, null=True, default=None)
    Attendance = models.IntegerField(blank=True, null=True, default=None)
