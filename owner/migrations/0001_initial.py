
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default=None, max_length=100)),
                ('Age', models.IntegerField(default=None)),
                ('Gender', models.CharField(default=None, max_length=12)),
                ('Address', models.CharField(default=None, max_length=100)),
                ('Mob', models.CharField(default=None, max_length=13)),
                ('Email', models.EmailField(default=None, max_length=100)),
                ('Department', models.CharField(default=None, max_length=100)),
                ('University', models.CharField(default=None, max_length=100)),
                ('Dob', models.DateField(default=None)),
                ('Phd_Reg', models.IntegerField(default=None)),
                ('Phd_Joining_Date', models.DateField(default=None)),
                ('Research_Topic', models.CharField(default=None, max_length=100)),
                ('Research_Guide', models.CharField(default=None, max_length=100)),
                ('Guide_Mail', models.EmailField(default=None, max_length=100)),
                ('Guide_Phone', models.CharField(default=None, max_length=13)),
                ('Eligibility', models.BooleanField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserId', models.CharField(max_length=100)),
                ('Photo', models.ImageField(upload_to='pics')),
                ('Achievements', models.TextField()),
                ('PaymentStatus', models.BooleanField(default=False)),
                ('PaymentDetails', models.FileField(default=None, upload_to='files')),
                ('Marks', models.IntegerField(blank=True, default=None, null=True)),
                ('Attendance', models.IntegerField(blank=True, default=None, null=True)),
                ('ApplicationId', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='owner.applicants')),
            ],
        ),
    ]