from django.shortcuts import render
from owner.models import Applicants
from django.contrib.auth.models import User,auth

# Create your views here.

def register(request):
    return render(request,'user/register_form.html')

def regSuccess(request):
     userObj=Applicants()
     userObj.Name=request.POST['Name']
     userObj.Age=request.POST['Age']
     userObj.Gender=request.POST['Gender']
     userObj.Address=request.POST['Address']
     userObj.Email = request.POST['Email']
     userObj.Department = request.POST['Department']

     userObj.save()

     return render(request,'user/reg_complete.html')










