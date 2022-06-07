from django.shortcuts import render
from owner.models import Applicants
from django.contrib.auth.models import User,auth
from django.http import JsonResponse

# Create your views here.

def register(request):

    if request.method=='POST':
        Name = request.POST['Name']
        Age = request.POST['Age']
        Gender = request.POST['Gender']
        Address = request.POST['Address']
        Email = request.POST['Email']
        Department = request.POST['Department']

        if Applicants.objects.filter(Email=Email).exists():

            return JsonResponse(

            {'success': 'error'},
            safe=False
            )

        else:

            return JsonResponse(

            {'success': 'pass'},
            safe=False
            )




    else:
        return render(request,'user/register_form.html')


def regSuccess(request):
    return render (request,'user/reg_complete.html')














