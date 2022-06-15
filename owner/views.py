from email import message
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Applicants, Candidates, Marks, Subjects
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import django.contrib.messages as messages
from django.contrib.postgres.search import SearchVector

# Create your views here.


def dashboard(request):
    return render(request, 'owner/dashboard.html')



def approve(request):
# coded by Hana
    if request.method == 'POST':

        search_vector = SearchVector('Name', 'Phd_Reg')
        Searchfield=request.POST['name']



        users = Applicants.objects.annotate(search=search_vector).filter(search=Searchfield)
        return render(request, 'owner/verify.html', {'users': users, 'message': 'User not found'})
    else:
        users = Applicants.objects.all()

        users = reversed(users)

        return render(request, 'owner/verify.html', {'users': users ,'message': 'User not found'})


def individual_view(request, userid):
    print(userid)
    selected_user = Applicants.objects.get(id=userid)
    return render(request, 'owner/individual.html', {'individual': selected_user})

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
    return render(request, 'owner/paymentstatus.html', {'users': users,'message': 'User not found'})

# payment verification done by akhila
def user_verify_view(request,userid):
    print(userid)
    user_det = Candidates.objects.get(id=userid)
    return render(request, 'owner/user_detail.html', {'person_details': user_det})

def denial(request, userid):
    print(userid)
    user = Candidates.objects.get(id=userid)
    user.PaymentStatus = False
    user.save()
    email = user.ApplicationId.Email
    message = f" Your profile stands incomplete. As payment proof being not verified"

    email = EmailMessage(
        'profile incomplete',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
    )

    email.fail_silently = False
    email.send()

    return redirect('payment')

def verified(request, userid):
    user = Candidates.objects.get(id=userid)
    user.PaymentStatus = True
    user.save()

    email = user.ApplicationId.Email

    message = f" Your payment verification has completed"

    email = EmailMessage(
        'your profile verified',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
    )

    email.fail_silently = False
    email.send()

    return redirect('payment')

# User management by Sharun

def user_manage(request):
    users = Applicants.objects.all()
    return render(request, 'owner/user_manage.html', {'users': users})


def search_user(request):
    if request.method == 'GET':
        searched_user = request.GET['search_data']
        requested_user = Applicants.objects.filter(Email=searched_user)
        if requested_user:
            return render(request, 'owner/user_manage.html', {'users': requested_user, 'message': 'User found'})
        else:
            users = Applicants.objects.all()
            return render(request, 'owner/user_manage.html', {'users': users, 'message': 'User not found'})


def view_user(request, email):
    user = Candidates.objects.filter(Email=email)[:1].get()
    return render(request, 'owner/view_user.html', {'user': user})


def update_user(request, email):
    # TODO: Update user details
    pass


def delete_user(request, userid):
    try:
        Candidates.objects.get(ApplicationId=userid).delete()
        Applicants.objects.filter(id=userid).delete()
        messages.success(request, 'User deleted successfully')
    except:
        messages.error(request, 'Error occured while deleting user')
    return redirect('user_manage')

#coded by devaprasad
def mark_upload(request):
    users = Candidates.objects.all()
    subjects = Subjects.objects.all()
    marks = Marks.objects.all()
    if request.method == 'POST':
        pass
    else:
        return render(request, 'owner/mark_upload.html', {'users': users,'marks':marks,'subjects':subjects})

def individual_mark_upload(request,userid):
    user = Candidates.objects.get(id=userid)
    if request.method == 'POST':
        Subject  = request.POST['subject']
        Attendance = int(request.POST['attendance'])
        Assignment1Mark =int(request.POST['assignment1'])
        Assignment2Mark = int(request.POST['assignment2'])
        GdMark = int(request.POST['gd'])
        CpMark = int(request.POST['cp'])

        sub = Subjects.objects.get(SubjectName=Subject)
        total_attendance = int(sub.TotalHour)
        print(total_attendance)

        attendance_percentage = (Attendance/total_attendance)*100
        print(attendance_percentage)
        if attendance_percentage >= 95:
            a_mark = 5
        elif attendance_percentage >=90:
            a_mark = 4
        elif attendance_percentage >=85:
            a_mark = 3
        elif attendance_percentage >=80:
            a_mark = 2
        elif attendance_percentage >=75:
            a_mark = 1
        else:
            a_mark = 0

        total_assignment = Assignment1Mark+Assignment2Mark
        total = a_mark+Assignment1Mark+Assignment2Mark+GdMark+CpMark
        user_mark = Marks.objects.create(StudentId=user, SubjectId=sub,Attendance=Attendance,AttendancePercentage=attendance_percentage, AttendanceMark=a_mark, Assignment1Mark=Assignment1Mark, Assignment2Mark=Assignment2Mark,TotalAssignmentMark=total_assignment, GdMark=GdMark,CpMark=CpMark,Total=total )
        user_mark.save()
        return redirect('mark_upload')

    else:
        subjects = Subjects.objects.all()
        return render(request, 'owner/mark_upload_form.html', {'user': user, 'subjects': subjects})


#coded by Hana
def subjects_edit(request):

    if request.method == 'POST':
        Subjectname=request.POST['subjectname']
        Totalhour=request.POST['totalhours']

        subject=Subjects()
        subject.SubjectName=Subjectname
        subject.TotalHour=Totalhour

        subject.save()

        return redirect('subjects_edit')

    else:
        subjects = Subjects.objects.all().order_by('id')
        return render(request, 'owner/subjects.html',{'subjects': subjects})

def subject_delete(request,subjectid):


    Subjects.objects.get(id=subjectid).delete()

    return redirect('subjects_edit')

def subject_update(request,subjectid):

    if request.method == 'POST':
        subjectname=request.POST['subjectname']
        totalhour=request.POST['totalhours']

        subject=Subjects.objects.get(id=subjectid)

        subject.SubjectName=subjectname
        subject.TotalHour=totalhour
        subject.save()



        return redirect('subjects_edit')


