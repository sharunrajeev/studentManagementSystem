from email import message
from django.contrib.auth.models import User,auth
from django.shortcuts import render, redirect
from .models import Applicants, Candidates, Marks, Subjects
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import django.contrib.messages as messages
from django.contrib.postgres.search import SearchVector
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum

# Create your views here.

#Coded by Hana
def adminlogin(request):

    # if request.method == 'POST':
    #     username = request.POST['Username']
    #     password = request.POST['Password']
    #
    #     user = auth.authenticate(username=username, password=password,is_staff =True)
    #
    #     if user is not None:
    #         auth.login(request, user)
    #         request.session['username'] = username
    #         return redirect('/owner/approve')
    #     else:
    #         messages.info(request, 'Invalid credentials')
    #         return redirect('/owner/adminlogin')
    #
    # else:
    #     return render(request, 'owner/adminlogin.html')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password, is_staff=True)

        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            return JsonResponse(
                {'success': True},
                safe=False
            )

        else:

            print("Invalid Credentials")
            return JsonResponse(
                {'success': False},
                safe=False
            )

    else:
        return render(request, 'owner/adminlogin.html')

def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('/owner/adminlogin')

def dashboard(request):
    return render(request, 'owner/dashboard.html')


def approve(request):
    # coded by Hana

    if request.method == 'POST':

        search_vector = SearchVector('Name', 'Phd_Reg')
        Searchfield = request.POST['name']

        users = Applicants.objects.annotate(search=search_vector).filter(search=Searchfield)
        return render(request, 'owner/verify.html', {'users': users, 'message': 'User not found'})
    else:
        users = Applicants.objects.all()

        users = reversed(users)

        return render(request, 'owner/verify.html', {'users': users})


def individual_view(request, userid):
    print(userid)
    selected_user = Applicants.objects.get(id=userid)
    return render(request, 'owner/individual.html', {'individual': selected_user})


def reject(request, userid):
    print(userid)
    user = Applicants.objects.get(id=userid)
    user.Eligibility = False
    user.save()
    name = user.Name
    email = user.Email
    message = f"Dear {name}," \
              f"\nAfter carefully reviewing your application, we regret to inform you that we are not offering you admission currently to the applied course " \
              f"We’d like to congratulate you on your impressive academic accomplishments and are confident you will continue to pursue excellence in your studies. " \
              f"Thank you for your time and effort in applying and we wish you the best of luck in your academic future!\n\n" \
              f"\nRegards\n" \
              f"CUSAT "

    email = EmailMessage(
        'Regarding the selection process',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
    )

    email.fail_silently = False
    email.send()

    return redirect('approve')

    # 2nd phase : coded by devaprasad
def select(request, userid):
    user = Applicants.objects.get(id=userid)
    user.Eligibility = True

    user.save()

    email = user.Email
    SubjectName = user.Subject

    subject = Subjects.objects.get(SubjectName = SubjectName)



    user_candidates = Candidates()
    user_candidates.ApplicationId = user
    user_candidates.SubjectId = subject
    user_candidates.UserId = userid
    user_candidates.save()

    # register number creating
    year = subject.Year
    reg_model = year * 1000
    candidate = Candidates.objects.get(UserId = userid)
    register_number = candidate.Register_Number
    reg_num = register_number + reg_model
    user_candidates.RegNumber = reg_num

    user_candidates.save()



    password = User.objects.make_random_password()
    username = reg_num
    name = user.Name
    candidate = User.objects.create_user(
        first_name=name, username=username, password=password, email=email)
    candidate.save()

    message = f"Dear {name}, \n" \
              f"\nWe are glad to inform you that, your application for 'Research and Publication Ethics Course Work Program'" \
              f" by 'PROF. N.R. MADAVA MENON INTERDISCIPLINARY CENTRE FOR RESEARCH ETHICS AND PROTOCOLS,CUSAT' have been selected." \
              f"Your Username and Password for Further processes have been provided with this E-mail." \
              f"Please complete the registration process and confirm your allotment before the last date.\n"\
              f" \nYour username : {reg_num}\n Your password: {password}\n\n" \
              f"\nRegards\n" \
              f"CUSAT."

    email = EmailMessage(
        'Greetings! You have selected',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
    )

    email.fail_silently = False
    email.send()

    return redirect('approve')


# Coded By Hana, Akhila
def payment(request):
    if request.method == 'POST':

        Searchfield = request.POST['name']
        users = Candidates.objects.filter(ApplicationId__Phd_Reg__contains=Searchfield)|Candidates.objects.filter(ApplicationId__Name__icontains=Searchfield)

        return render(request, 'owner/paymentstatus.html', {'users': users, 'message': 'User not found'})
    else:
        users = Candidates.objects.all()

        users = reversed(users)

        return render(request, 'owner/paymentstatus.html', {'users': users, 'message': 'User not found'})


# payment verification done by akhila
# responsive page

def user_verify_view(request, userid):
    print(userid)
    user_det = Candidates.objects.get(id=userid)
    if user_det.PaymentDetails:
        pay_val = 1
    else:
        pay_val = 0
    return render(request, 'owner/user_detail.html', {'person_details': user_det, 'pay_val': pay_val})


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


# coded by devaprasad
# def mark_upload(request):
#     users = Candidates.objects.all()
#     subjects = Subjects.objects.all()
#     marks = Marks.objects.all()
#     if request.method == 'POST':
#         pass
#     else:
#         return render(request, 'owner/mark_upload.html', {'users': users, 'marks': marks, 'subjects': subjects})
# coded by dp
def show_subjects(request):
    subjects = Subjects.objects.all().order_by('id')
    if request.method == 'POST':
        Searchfield = request.POST['name']
        subjects = Subjects.objects.filter(SubjectName=Searchfield)
        return render(request, 'owner/show_subjects.html', {'subjects': subjects})

    else:

        subjects = Subjects.objects.all().order_by('id')
        return render(request, 'owner/show_subjects.html', {'subjects': subjects})



# Edited by Akhila
def mark_upload(request,subjectid):
    users = Candidates.objects.all().order_by('RegNumber')
    subjects = Subjects.objects.all()
    marks = Marks.objects.all()
    if request.method == 'POST':
        pass
        Searchfield = request.POST['name']
        users = Candidates.objects.filter(ApplicationId__Phd_Reg__contains=Searchfield) | Candidates.objects.filter(
            ApplicationId__Name__icontains=Searchfield)

        return render(request, 'owner/mark_upload.html', {'users': users, 'marks': marks, 'subjects': subjects})

    else:
        return render(request, 'owner/mark_upload.html', {'users': users, 'marks': marks, 'subjects': subjects})


def individual_mark_upload(request, userid):
    user = Candidates.objects.get(Register_Number=userid)
    if request.method == 'POST':
        Subject = request.POST['subject']
        Attendance = int(request.POST['attendance'])
        Assignment1Mark = int(request.POST['assignment1'])
        Assignment2Mark = int(request.POST['assignment2'])
        GdMark = int(request.POST['gd'])
        CpMark = int(request.POST['cp'])

        attendance_percentage, a_mark, total_assignment, total, sub = mark_calculation(Subject, Attendance,
                                                                                       Assignment1Mark,
                                                                                       Assignment2Mark, GdMark, CpMark)

        user_mark = Marks.objects.create(StudentId=user, SubjectId=sub, Attendance=Attendance,
                                         AttendancePercentage=attendance_percentage, AttendanceMark=a_mark,
                                         Assignment1Mark=Assignment1Mark, Assignment2Mark=Assignment2Mark,
                                         TotalAssignmentMark=total_assignment, GdMark=GdMark, CpMark=CpMark,
                                         Total=total)
        user_mark.save()
        candidate = Candidates.objects.get(id=userid)
        total_table = Marks.objects.filter(StudentId = candidate).aggregate(Sum('Total'))
        total_marks = total_table.get('Total__sum')
        print(total_marks)
        candidate.Marks = int(total_marks)

        candidate.save()
        return redirect('mark_upload')

    else:
        subjects = Subjects.objects.all()
        return render(request, 'owner/mark_upload_form.html', {'user': user, 'subjects': subjects})


def mark_edit(request, userid):
    if request.method == 'POST':
        pass
    else:
        user = Candidates.objects.get(id=userid)
        marks = Marks.objects.filter(StudentId=user).order_by('id')
        return render(request, 'owner/mark_edit.html', {'User': user, 'marks': marks})


def mark_update(request, markid):
    if request.method == 'POST':
        Attendance = int(request.POST['attendance'])
        Assignment1Mark = int(request.POST['assignment1'])
        Assignment2Mark = int(request.POST['assignment2'])
        GdMark = int(request.POST['gd'])
        CpMark = int(request.POST['cp'])

        mark = Marks.objects.get(id=markid)
        userid = mark.StudentId.id

        Subject = mark.SubjectId.SubjectName
        attendance_percentage, a_mark, total_assignment, total, sub = mark_calculation(Subject, Attendance,
                                                                                       Assignment1Mark,
                                                                                       Assignment2Mark, GdMark, CpMark)
        mark.AttendancePercentage = attendance_percentage
        mark.AttendanceMark = a_mark
        mark.TotalAssignmentMark = total_assignment
        mark.Total = total
        mark.Attendance = Attendance
        mark.Assignment1Mark = Assignment1Mark
        mark.Assignment2Mark = Assignment2Mark
        mark.GdMark = GdMark
        mark.CpMark = CpMark

        mark.save()

        candidate = Candidates.objects.get(id=userid)
        total_table = Marks.objects.filter(StudentId = candidate).aggregate(Sum('Total'))
        total_marks = total_table.get('Total__sum')
        print(total_marks)
        candidate.Marks = int(total_marks)

        candidate.save()
        return redirect('mark_upload')

        return redirect(f"/owner/mark_edit/{userid}")


def mark_delete(request, markid):
    mark = Marks.objects.get(id=markid)
    userid = mark.StudentId.id
    mark.delete()
    return redirect(f"/owner/mark_edit/{userid}")


def mark_calculation(Subject, Attendance, Assignment1Mark, Assignment2Mark, GdMark, CpMark):
    sub = Subjects.objects.get(SubjectName=Subject)
    total_attendance = int(sub.TotalHour)

    attendance_percentage = (Attendance / total_attendance) * 100
    print(attendance_percentage)
    if attendance_percentage >= 95:
        a_mark = 5
    elif attendance_percentage >= 90:
        a_mark = 4
    elif attendance_percentage >= 85:
        a_mark = 3
    elif attendance_percentage >= 80:
        a_mark = 2
    elif attendance_percentage >= 75:
        a_mark = 1
    else:
        a_mark = 0

    total_assignment = Assignment1Mark + Assignment2Mark
    total = a_mark + Assignment1Mark + Assignment2Mark + GdMark + CpMark

    return attendance_percentage, a_mark, total_assignment, total, sub


# coded by Hana
# 2nd phase : coded by devaprasad
def subjects_edit(request):
    if request.method == 'POST':
        Subjectname = request.POST['subjectname']
        Totalhour = request.POST['totalhours']
        Year  = request.POST['year']
        subject = Subjects()
        subject.SubjectName = Subjectname
        subject.TotalHour = Totalhour
        subject.Year = Year

        subject.save()

        return redirect('subjects_edit')

    else:
        subjects = Subjects.objects.all().order_by('id')
        return render(request, 'owner/subjects.html', {'subjects': subjects})


def subject_delete(request, subjectid):
    Subjects.objects.get(id=subjectid).delete()

    return redirect('subjects_edit')


def subject_update(request, subjectid):
    if request.method == 'POST':
        subjectname = request.POST['subjectname']
        totalhour = request.POST['totalhours']
        year = request.POST['year']

        subject = Subjects.objects.get(id=subjectid)

        subject.SubjectName = subjectname
        subject.TotalHour = totalhour
        subject.save()

        return redirect('subjects_edit')




# report generation coded by devaprasad

# def show_report(request):
#     subjects = Subjects.objects.all().order_by('id')
#
#     return render(request,'owner/show_report.html',{'subjects':subjects})

def show_report(request):
    subjects = Subjects.objects.all().order_by('id')
    if request.method == 'POST':
        Searchfield = request.POST['name']
        subjects = Subjects.objects.filter(SubjectName=Searchfield)
        return render(request, 'owner/show_report.html', {'subjects': subjects})

    else:

        subjects = Subjects.objects.all().order_by('id')
        return render(request, 'owner/show_report.html', {'subjects': subjects})


def report(request,subjectid):
     subject = Subjects.objects.get(id=subjectid)
     marks = Marks.objects.filter(SubjectId = subject).order_by('id')
     return render(request, 'owner/report.html' , {'marks':marks,'subject':subject})

def report_download(request,subjectid):
    subject = Subjects.objects.get(id=subjectid)
    marks = Marks.objects.filter(SubjectId=subject).order_by('id')

    template_path = 'owner/pdf_report.html'
    context = {'marks':marks,'subject':subject}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="subject_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def report_mark(request):
    marks = Marks.objects.all()
    users = Candidates.objects.all()
    subjects = Subjects.objects.all()
    return render(request,'owner/report_mark.html',{'marks':marks,'users':users,'subjects':subjects})

def report_mark_download(request):
    marks = Marks.objects.all()
    users = Candidates.objects.all()
    subjects = Subjects.objects.all()



    template_path = 'owner/pdf_report_mark.html'
    context = {'marks':marks,'subjects':subjects,'users':users}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="subject_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def report_attendance(request):
    marks = Marks.objects.all()
    users = Candidates.objects.all()
    subjects = Subjects.objects.all()
    return render(request,'owner/report_attendance.html',{'marks':marks,'users':users,'subjects':subjects})

def report_attendance_download(request):
    marks = Marks.objects.all()
    users = Candidates.objects.all()
    subjects = Subjects.objects.all()



    template_path = 'owner/pdf_report_attendance.html'
    context = {'marks':marks,'subjects':subjects,'users':users}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="subject_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

