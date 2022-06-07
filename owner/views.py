

from django.shortcuts import render,redirect
from .models import Applicants
# from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def approve(request):

    users=Applicants.objects.all()

    return render (request,'owner/verify.html',{'users':users})

def reject(request,userid):
    print(userid)
    user=Applicants.objects.get(id=userid)
    user.delete()

    return redirect ('approve')

def select(request,userid):

    user=Applicants.objects.get(id=userid)
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


    return redirect ('approve')







