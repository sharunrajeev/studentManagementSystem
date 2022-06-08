from django.shortcuts import render
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
        Email = request.POST['Email']
        Department = request.POST['Department']

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
            user_obj.Email = Email
            user_obj.Department = Department

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
    return render(request, 'user/auth/login.html')
