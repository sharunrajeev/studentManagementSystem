from django.db import models


# Create your models here.
class Subjects(models.Model):
    SubjectName = models.CharField(max_length=100, default=None)
    TotalHour = models.IntegerField(default=None)


class Batches(models.Model):
    Batch_Name = models.CharField(max_length=100, default=None, null=True)
    Month = models.CharField(max_length=100, default=None)
    Year = models.IntegerField(default=None)
    CommenceDate = models.DateField(default=None)
    Active = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.Active:
            try:
                temp = Batches.objects.get(Active=True)
                if self != temp:
                    temp.Active = False
                    temp.save()
            except Batches.DoesNotExist:
                pass
        super(Batches, self).save(*args, **kwargs)

    def __str__(self):
        return self.Batch_Name


class Applicants(models.Model):
    Batch = models.ForeignKey(Batches, on_delete=models.CASCADE, default=False)
    Name = models.CharField(max_length=100, default=None)
    Gender = models.CharField(max_length=12, default=None)
    Address = models.CharField(max_length=100, default=None)
    Mob = models.CharField(max_length=13, default=None)
    Email = models.EmailField(max_length=100, default=None)
    Institution = models.CharField(max_length=100, default=None)
    University = models.CharField(max_length=100, default=None)
    Dob = models.DateField(default=None)
    Phd_Reg = models.IntegerField(default=None)
    Phd_Joining_Date = models.DateField(default=None)
    Research_Topic = models.CharField(max_length=100, default=None)
    Research_Guide = models.CharField(max_length=100, default=None)
    Guide_Mail = models.EmailField(max_length=100, default=None,null=True)
    Guide_Phone = models.CharField(max_length=13, default=None,null=True)
    Guide_Dpt =  models.CharField(max_length=100, default=None)

    Co_Guide = models.BooleanField(blank=True, null=True, default=None)

    Co_Guide_Name = models.CharField(max_length=100, default=None,null=True)
    Co_Guide_Mail = models.EmailField(max_length=100, default=None, null=True)
    Co_Guide_Phone = models.CharField(max_length=13, default=None, null=True)
    Co_Guide_Dpt = models.CharField(max_length=100, default=None, null=True)

    Eligibility = models.BooleanField(blank=True, null=True, default=None)
    Reject = models.BooleanField(blank=True, null=True, default=False)
    Cusatian = models.BooleanField(blank=True, null=True, default=None)
    Cusat_Id = models.FileField(upload_to='files', blank=True, null=True, default=None)
    Short_Name =  models.CharField(max_length=100, default=None,null=True)


class Payments(models.Model):
    PaymentName = models.CharField(max_length=100, default=None)
    FreeForCusat = models.BooleanField(blank=True, null=True, default=None)


class Candidates(models.Model):
    ApplicationId = models.ForeignKey(Applicants, on_delete=models.CASCADE, default=False)
    # SubjectId = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=False)
    Register_Number = models.AutoField(default=None, primary_key=True)
    RegNumber = models.IntegerField(blank=True, null=True, default=None)
    UserId = models.IntegerField(default=None, blank=True, null=True)
    Photo = models.ImageField(upload_to='pics')
    Achievements = models.TextField()
    Marks = models.IntegerField(blank=True, null=True, default=None)
    Attendance = models.IntegerField(blank=True, null=True, default=None)
    Dropout = models.BooleanField(blank=True, null=True, default=False)


class UserPayments(models.Model):
    StudentId = models.ForeignKey(Candidates, on_delete=models.CASCADE, default=False)
    PaymentId = models.ForeignKey(Payments, on_delete=models.CASCADE, default=False)
    PaymentStatus = models.BooleanField(blank=True, null=True, default=None)
    PaymentDetails = models.FileField(upload_to='files', blank=True, null=True, default=None)


class Marks(models.Model):
    StudentName = models.CharField(max_length=100, default=None, null=True)
    StudentReg = models.IntegerField(blank=True, null=True, default=None)
    StudentId = models.ForeignKey(Candidates, on_delete=models.CASCADE, default=False)
    Attendance = models.IntegerField(default=None)
    AttendancePercentage = models.IntegerField(default=None, blank=True, null=True)
    AttendanceMark = models.IntegerField(default=None, blank=True, null=True)
    Assignment1Mark = models.IntegerField(default=None)
    Assignment2Mark = models.IntegerField(default=None)
    TotalAssignmentMark = models.IntegerField(default=None, blank=True, null=True)
    GdMark = models.IntegerField(default=None)
    CpMark = models.IntegerField(default=None)
    Total = models.IntegerField(default=None, blank=True, null=True)
    ExternalMark = models.IntegerField(default=0, blank=True, null=True)

