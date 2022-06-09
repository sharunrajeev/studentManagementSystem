from pyexpat.errors import messages
from django.shortcuts import redirect, render
from owner.models import Applicants
from django.contrib.auth.models import User, auth
from django.http import JsonResponse


# Create your views here.

def register(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Age = request.POST['Age']
        Gender = request.POST['Gender']
        Address = request.POST['Address']
        Mob = request.POST['Mob']
        Email = request.POST['Email']
        Department = request.POST['Department']
        University = request.POST['University']
        Dob = request.POST['Dob']
        Phd_Reg = request.POST['Phd_Reg']
        Phd_Joining_Date = request.POST['Phd_Joining_Date']
        Research_Topic = request.POST['Research_Topic']
        Research_Guide= request.POST['Research_Guide']
        Guide_Mail = request.POST['Guide_Mail']


        if Applicants.objects.filter(Email=Email).exists():
            return JsonResponse(
                {'success': 'error'},
                safe=False
            )
        else:
            user_obj = Applicants()
            user_obj.Name = Name
            user_obj.Age = Age
            user_obj.Gender = Gender
            user_obj.Address = Address
            user_obj.Mob = Mob
            user_obj.Email = Email
            user_obj.Department = Department
            user_obj.University = University
            user_obj.Dob = Dob
            user_obj.Phd_Reg = Phd_Reg
            user_obj.Phd_Joining_Date = Phd_Joining_Date
            user_obj.Research_Topic = Research_Topic
            user_obj.Research_Guide = Research_Guide
            user_obj.Guide_Mail = Guide_Mail

            user_obj.save()

            return JsonResponse(

                {'success': 'pass'},
                safe=False
            )

    else:
        return render(request, 'user/register_form.html')


def reg_success(request):
    return render(request, 'user/reg_complete.html')


# Sharun
def login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        print(username, password)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/user/dashboard')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('/user/login')

    else:
        return render(request, 'user/auth/login.html')


def dashboard(request):
    return render(request, 'user/dashboard.html')