
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from .models import Applicants,Candidates
# from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def approve(request):

    users=Applicants.objects.all()

    return render (request,'owner/verify.html',{'users':users})

def reject(request,userid):
    print(userid)
    user = Applicants.objects.get(id=userid)
    user.Eligibility = False
    user.save()
    return redirect ('approve')

def select(request,userid):

    user=Applicants.objects.get(id=userid)
    user.Eligibility = True
    user.save()
    print(user.Email)
    # email=EmailMessage(
    #     'subjects',
    #     'body',
    #     'settings.EMAIL_HOST_USER',
    #     ['devaprasadmohan@gmail.com'],
    #
    #
    # )

    # email.fail_silently=False
    # email.send()
    user_candidates = Candidates()
    user_candidates.ApplicationId = user
    user_candidates.save()
    password = User.objects.make_random_password()
    email = user.Email
    username = user.Email
    name = user.Name
    candidate = User.objects.create_user(first_name=name, username=username, password=password, email=email)
    candidate.save()
    return redirect ('approve')







