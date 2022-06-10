
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Applicants, Candidates
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.


def dashboard(request):
    return render(request, 'owner/dashboard.html')


def approve(request):

    users = Applicants.objects.all()

    users = reversed(users)

    return render(request, 'owner/verify.html', {'users': users})


def reject(request, userid):
    print(userid)
    user = Applicants.objects.get(id=userid)
    user.Eligibility = False
    user.save()
    email = user.Email
    message = f"We regret to inform you that you have not been selected."

    email = EmailMessage(
        'Regarding the selection process',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
    )

    email.fail_silently = False
    email.send()

    return redirect('approve')


def select(request, userid):

    user = Applicants.objects.get(id=userid)
    user.Eligibility = True
    user.save()

    email = user.Email

    user_candidates = Candidates()
    user_candidates.ApplicationId = user
    user_candidates.UserId = email
    user_candidates.save()

    password = User.objects.make_random_password()
    username = user.Email
    name = user.Name
    candidate = User.objects.create_user(
        first_name=name, username=username, password=password, email=email)
    candidate.save()

    message = f"Your username:{email}\n Your password: {password}"

    email = EmailMessage(
        'You have been selected',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
    )

    email.fail_silently = False
    email.send()


    return redirect('approve')

  


def payment(request):


    if request.method == 'POST':
        Name = request.POST['name']
        users = Candidates.objects.filter(ApplicationId__Name__icontains=Name)
    else:
        users = Candidates.objects.all()

    users = reversed(users)
    return render(request, 'owner/paymentstatus.html',{'users':users})




def user_manage(request):
    users=Applicants.objects.all()
    return render(request, 'owner/user_manage.html', {'users': users})


def search_user(request):
    if request.method == 'GET':
        searched_user = request.GET['search_data']
        requested_user = Applicants.objects.filter(Email=searched_user)
        if requested_user:
            return render(request, 'owner/user_manage.html', {'users': requested_user})
        else:
            users=Applicants.objects.all()
            return render(request, 'owner/user_manage.html', {'users': users})
