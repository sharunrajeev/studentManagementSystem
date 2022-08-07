from email import message
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from .models import Applicants, Candidates, Marks, Subjects, Payments, UserPayments, Batches
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
from datetime import datetime

# Create your views here.

total_attendance = 20


# Coded by Hana
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
    if 'username_admin' in request.session:
        return redirect('/owner/approve')
    else:
        if request.method == 'POST':

            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password, is_staff=True)

            if user is not None:
                auth.login(request, user)
                request.session['username_admin'] = username
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
    if 'username_admin' in request.session:
        request.session.flush()
    return redirect('/owner/adminlogin')


# def dashboard(request):
#     if 'username_admin' in request.session:
#         applicantCount = Applicants.objects.count()
#         candidateCount = Candidates.objects.count()
#         subjectCount = Subjects.objects.count()
#         return render(request, 'owner/dashboard.html', {'totalApplicants': applicantCount, 'totalCandidates': candidateCount, 'totalCourses': subjectCount})
#     else:
#         return render(request, 'owner/adminlogin.html')


def approve(request):
    # coded by Hana
    if 'username_admin' in request.session:
        if request.method == 'POST':

            search_vector = SearchVector('Name', 'Phd_Reg')
            Searchfield = request.POST['name']

            users = Applicants.objects.annotate(search=search_vector).filter(search=Searchfield)
            return render(request, 'owner/verify.html', {'users': users, 'message': 'User not found'})
        else:
            Latest_Batch = Batches.objects.all().order_by('-id').first()
            users = Applicants.objects.filter(Batch=Latest_Batch)

            users = reversed(users)

            users_unselected = Applicants.objects.filter(Batch = Latest_Batch).filter(Eligibility = '').order_by('Name')

            return render(request, 'owner/verify.html', {'users': users,'unselected':users_unselected})
    else:
        return redirect('/owner/adminlogin')


def individual_view(request, userid):
    if 'username_admin' in request.session:
        selected_user = Applicants.objects.get(id=userid)

        users = Applicants.objects.all()
        candidate = ""
        if selected_user.Eligibility == True and selected_user.Reject == False:
            candidate = Candidates.objects.get(UserId=userid)
        return render(request, 'owner/individual.html',
                      {'individual': selected_user, 'users': users, 'candidate': candidate})

    else:
        return redirect('/owner/adminlogin')


def reject(request, userid):
    if 'username_admin' in request.session:
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
    else:
        return redirect('/owner/adminlogin')

    # 2nd phase : coded by devaprasad

def short_name(request,userid):
    if 'username_admin' in request.session:
        if request.method == 'POST':
            short_name = request.POST['short_name']
            user = Applicants.objects.get(id=userid)
            user.Short_Name = short_name
            user.save()
            return redirect(f'/owner/approve/{userid}')
    else:
        return redirect('/owner/adminlogin')

def select(request, userid):
    if 'username_admin' in request.session:
        user = Applicants.objects.get(id=userid)
        user.Eligibility = True

        user.save()

        email = user.Email

        user_candidates = Candidates()
        user_candidates.ApplicationId = user

        user_candidates.UserId = userid
        user_candidates.save()

        # register number creating
        date = datetime.now()
        month = date.month
        year = date.year
        year_model = (year % 100) * 100000
        month_model = month * 1000

        candidate = Candidates.objects.get(UserId=userid)
        register_number = candidate.Register_Number
        reg_num = register_number + year_model + month_model
        user_candidates.RegNumber = reg_num

        user_candidates.save()

        password = User.objects.make_random_password()
        username = reg_num
        name = user.Name
        candidate = User.objects.create_user(
            first_name=name, username=username, password=password, email=email)
        candidate.save()
        login_link = "https://nrmcentre-sms.herokuapp.com/user/login"
        message = f"Dear {name}, \n" \
                  f"\nWe are glad to inform you that, your application for 'Research and Publication Ethics Course Work Program'" \
                  f" by 'PROF. N.R. MADAVA MENON INTERDISCIPLINARY CENTRE FOR RESEARCH ETHICS AND PROTOCOLS,CUSAT' have been selected." \
                  f"Your Username and Password for Further processes have been provided with this E-mail." \
                  f"Please complete the registration process and confirm your allotment before the last date.\n" \
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
    else:
        return redirect('/owner/adminlogin')


# new changes in payment, coded by Devaprasd
#
# def show_payment(request):
#     if 'username_admin' in request.session:
#         subjects = Subjects.objects.all().order_by('id')
#         if request.method == 'POST':
#             Searchfield = request.POST['name']
#             subjects = Subjects.objects.filter(SubjectName=Searchfield)
#             return render(request, 'owner/show_report.html', {'subjects': subjects})
#
#         else:
#
#             payments = Payments.objects.all().order_by('id')
#             return render(request, 'owner/show_payment.html', {'payments': payments})
#
#     else:
#         return redirect('/owner/adminlogin')

# Coded By Hana, Akhila
# def payment_subject(request,subjectid):
#     if 'username_admin' in request.session:
#         if request.method == 'POST':
#
#             Searchfield = request.POST['name']
#             users = Candidates.objects.filter(ApplicationId__Phd_Reg__contains=Searchfield) | Candidates.objects.filter(
#                 ApplicationId__Name__icontains=Searchfield)
#
#             return render(request, 'owner/paymentstatus.html', {'users': users, 'message': 'User not found'})
#         else:
#             users = Candidates.objects.filter(SubjectId__id =subjectid).order_by('Register_Number')
#
#             return render(request, 'owner/paymentstatus.html', {'users': users, 'message': 'User not found'})
#
#     else:
#         return redirect('/owner/adminlogin')

def payment_subject(request):
    if 'username_admin' in request.session:

        if request.method == 'POST':

            Searchfield = request.POST['name']
            users = Candidates.objects.filter(ApplicationId__Phd_Reg__contains=Searchfield) | Candidates.objects.filter(
                ApplicationId__Name__icontains=Searchfield)

            return render(request, 'owner/paymentstatus.html', {'users': users, 'message': 'User not found'})
        else:
            Latest_Batch = Batches.objects.all().order_by('-id').first()
            users = Candidates.objects.filter(ApplicationId__Batch=Latest_Batch).order_by('Register_Number')

            user_payments = UserPayments.objects.all()

            return render(request, 'owner/paymentstatus.html',
                          {'users': users, 'user_payments': user_payments, 'message': 'User not found'})

    else:
        return redirect('/owner/adminlogin')


# payment verification done by akhila
# responsive page

def user_verify_view(request, userid):
    if 'username_admin' in request.session:
        user_det = Candidates.objects.get(Register_Number=userid)
        # if user_det.PaymentDetails:
        #     pay_val = 1
        # else:
        #     pay_val = 0
        user_payments = UserPayments.objects.filter(StudentId=user_det)
        return render(request, 'owner/user_detail.html', {'person_details': user_det, 'user_payments': user_payments})

    else:
        return redirect('/owner/adminlogin')


def denial(request, userid):
    if 'username_admin' in request.session:

        # user = Candidates.objects.get(Register_Number=userid)
        user = UserPayments.objects.get(id=userid)
        candidate_id = user.StudentId.Register_Number
        user.PaymentStatus = False
        user.save()
        name = user.StudentId.ApplicationId.Name
        subject = user.StudentId.ApplicationId.Subject
        payment = user.PaymentId.PaymentName
        email = user.StudentId.ApplicationId.Email
        message = f"Dear {name}\n" \
                  f"\n Your profile stands incomplete for {payment} of the course {subject}." \
                  f" As the payment proof being not Uploaded the required recipt/ being not verified\n" \
                  f"\n\n Regards\n CUSAT"

        email = EmailMessage(
            'Your Payment incomplete',
            message,
            'settings.EMAIL_HOST_USER',
            [email],
        )

        email.fail_silently = False
        email.send()

        return redirect(f'/owner/payment/{candidate_id}')
    else:
        return redirect('/owner/adminlogin')


def verified(request, userid):
    if 'username_admin' in request.session:
        # user_canditate = Candidates.objects.get(Register_Number=userid)
        # user_id= user_candidate.id
        user = UserPayments.objects.get(id=userid)
        candidate_id = user.StudentId.Register_Number
        user.PaymentStatus = True
        user.save()
        name = user.StudentId.ApplicationId.Name
        # subject = user.StudentId.ApplicationId.Subject
        payment = user.PaymentId.PaymentName
        email = user.StudentId.ApplicationId.Email
        message = f"Dear {name} \n" \
                  f" \nYour payment verification has completed for {payment} of the course.\n" \
                  f"\n\n Regards\n CUSAT"

        email = EmailMessage(
            'Your payment proof verified',
            message,
            'settings.EMAIL_HOST_USER',
            [email],
        )

        email.fail_silently = False
        email.send()

        return redirect(f'/owner/payment/{candidate_id}')
    else:
        return redirect('/owner/adminlogin')


# User management by Sharun

def user_manage(request):
    if 'username_admin' in request.session:
        users = Applicants.objects.all()
        return render(request, 'owner/user_manage.html', {'users': users})
    else:
        return redirect('/owner/adminlogin')


def search_user(request):
    if 'username_admin' in request.session:
        if request.method == 'GET':
            searched_user = request.GET['search_data']
            requested_user = Applicants.objects.filter(Email=searched_user)
            if requested_user:
                return render(request, 'owner/user_manage.html', {'users': requested_user, 'message': 'User found'})
            else:
                users = Applicants.objects.all()
                return render(request, 'owner/user_manage.html', {'users': users, 'message': 'User not found'})

    else:
        return redirect('/owner/adminlogin')


def view_user(request, email):
    if 'username_admin' in request.session:
        user = Candidates.objects.filter(Email=email)[:1].get()
        return render(request, 'owner/view_user.html', {'user': user})
    else:
        return redirect('/owner/adminlogin')


def update_user(request, email):
    # TODO: Update user details
    if 'username_admin' in request.session:
        pass
    # code here
    else:
        return redirect('/owner/adminlogin')


def delete_user(request, userid):
    if 'username_admin' in request.session:

        user = Candidates.objects.get(Register_Number=userid)
        user.ApplicationId.Reject = True
        batch_id = user.ApplicationId.Batch.id
        user.ApplicationId.save()
        user.delete()
        messages.error(request, 'Error occured while deleting user')
        return redirect(f'/owner/user_edit/{batch_id}')
    else:
        return redirect('/owner/adminlogin')


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
def show_batches(request):
    if 'username_admin' in request.session:
        batches = Batches.objects.all().order_by('id')
        batches = reversed(batches)
        if request.method == 'POST':
            Searchfield = request.POST['name']

            batches = Batches.objects.filter(Batch_Name__icontains=Searchfield) | Batches.objects.filter(
                Month__icontains=Searchfield) | Batches.objects.filter(Year__icontains=Searchfield)
            return render(request, 'owner/show_batches.html', {'batches': batches})

        else:
            return render(request, 'owner/show_batches.html', {'batches': batches})

    else:
        return redirect('/owner/adminlogin')


# Edited by Akhila
# new editing devaprasad
def show_students(request):
    if 'username_admin' in request.session:
        Latest_Batch = Batches.objects.all().order_by('-id').first()
        users = Candidates.objects.filter(ApplicationId__Batch=Latest_Batch).order_by('RegNumber')

        marks = Marks.objects.all()
        if request.method == 'POST':

            Searchfield = request.POST['name']
            users = Candidates.objects.filter(ApplicationId__Phd_Reg__contains=Searchfield) | Candidates.objects.filter(
                ApplicationId__Name__icontains=Searchfield) | Candidates.objects.filter(
                Register_Number__contains=Searchfield)

            return render(request, 'owner/mark_upload.html', {'users': users, 'marks': marks})

        else:
            return render(request, 'owner/mark_upload.html', {'users': users, 'marks': marks})

    else:
        return redirect('/owner/adminlogin')


def individual_mark_upload(request, userid):
    global total_attendance

    if 'username_admin' in request.session:
        user = Candidates.objects.get(Register_Number=userid)

        if request.method == 'POST':

            Attendance = int(request.POST['attendance'])
            Assignment1Mark = int(request.POST['assignment1'])
            Assignment2Mark = int(request.POST['assignment2'])
            GdMark = int(request.POST['gd'])
            CpMark = int(request.POST['cp'])

            attendance_percentage, a_mark, total_assignment, total = mark_calculation(Attendance,
                                                                                      Assignment1Mark,
                                                                                      Assignment2Mark, GdMark, CpMark)

            user_mark = Marks.objects.create(StudentId=user, Attendance=Attendance,
                                             AttendancePercentage=attendance_percentage, AttendanceMark=a_mark,
                                             Assignment1Mark=Assignment1Mark, Assignment2Mark=Assignment2Mark,
                                             TotalAssignmentMark=total_assignment, GdMark=GdMark, CpMark=CpMark,
                                             Total=total)
            user_mark.save()

            total_table = Marks.objects.filter(StudentId=user).aggregate(Sum('Total'))
            total_marks = total_table.get('Total__sum')
            print(total_marks)
            user.Marks = int(total_marks)

            user.save()
            return redirect(f'/owner/show_students')

        else:

            return render(request, 'owner/mark_upload_form.html', {'user': user, 'total_attendance': total_attendance})
    else:
        return redirect('/owner/adminlogin')


def mark_edit(request, userid):
    global total_attendance
    if 'username_admin' in request.session:
        if request.method == 'POST':
            pass
        else:
            user = Candidates.objects.get(Register_Number=userid)
            marks = Marks.objects.filter(StudentId=user).order_by('id')
            return render(request, 'owner/mark_edit.html',
                          {'User': user, 'marks': marks, 'total_attendance': total_attendance})
    else:
        return redirect('/owner/adminlogin')


def mark_update(request, markid):
    if 'username_admin' in request.session:
        if request.method == 'POST':
            Attendance = int(request.POST['attendance'])
            Assignment1Mark = int(request.POST['assignment1'])
            Assignment2Mark = int(request.POST['assignment2'])
            GdMark = int(request.POST['gd'])
            CpMark = int(request.POST['cp'])
            ExternalMark = int(request.POST['ex_mark'])
            mark = Marks.objects.get(id=markid)
            userid = mark.StudentId.Register_Number

            attendance_percentage, a_mark, total_assignment, total = mark_calculation(Attendance,
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
            mark.ExternalMark = ExternalMark

            mark.save()

            candidate = Candidates.objects.get(Register_Number=userid)
            total_table = Marks.objects.filter(StudentId=candidate).aggregate(Sum('Total'))
            total_marks = total_table.get('Total__sum')
            print(total_marks)
            candidate.Marks = int(total_marks)

            candidate.save()

            user = Candidates.objects.get(Register_Number=userid)
            marks = Marks.objects.filter(StudentId=user).order_by('id')
            return render(request, 'owner/mark_edit.html',
                          {'User': user, 'marks': marks, 'message': "Mark Details updated successfully"})
    else:
        return redirect('/owner/adminlogin')


def mark_delete(request, markid):
    if 'username_admin' in request.session:
        mark = Marks.objects.get(id=markid)
        userid = mark.StudentId.Register_Number
        mark.delete()
        return redirect(f"/owner/mark_edit/{userid}")
    else:
        return redirect('/owner/adminlogin')


def mark_calculation(Attendance, Assignment1Mark, Assignment2Mark, GdMark, CpMark):
    global total_attendance

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

    return attendance_percentage, a_mark, total_assignment, total


# coded by Hana
# 2nd phase : coded by devaprasad
def batches_edit(request):
    if 'username_admin' in request.session:
        if request.method == 'POST':
            Month = request.POST['month']
            Year = request.POST['year']
            CommenceDate = request.POST['commencedate']

            batch = Batches()
            batch.Month = Month
            batch.Year = Year
            batch.CommenceDate = CommenceDate

            batch.save()
            counter_name()

            # subjects = Subjects.objects.all().order_by('id')
            # return render(request, 'owner/subjects.html',
            #               {'subjects': subjects, 'message': f"New Course {Subjectname} added successfully"})
            return redirect('/owner/batches_edit')
        else:
            batches = Batches.objects.all().order_by('id')
            batches = reversed(batches)

            return render(request, 'owner/batches.html', {'batches': batches})
    else:
        return redirect('/owner/adminlogin')


def counter_name():
    batches = Batches.objects.all()
    index = 1
    for batch in batches:
        batch.Batch_Name = "Batch " + str(index)
        index += 1
        batch.save()


# def subject_delete(request, subjectid):
#     Subjects.objects.get(id=subjectid).delete()
#
#     return redirect('subjects_edit')


def batch_update(request, batchid):
    if 'username_admin' in request.session:
        if request.method == 'POST':
            Month = request.POST['month']
            Year = request.POST['year']
            CommenceDate = request.POST['commencedate']

            batch = Batches.objects.get(id=batchid)
            batch.Month = Month
            batch.Year = Year
            batch.CommenceDate = CommenceDate

            batch.save()

            batches = Batches.objects.all().order_by('id')

            return render(request, 'owner/batches.html',
                          {'batches': batches, 'message': f" Batch details updated successfully"})

    else:
        return redirect('/owner/adminlogin')


# report generation coded by devaprasad

# def show_report(request):
#     subjects = Subjects.objects.all().order_by('id')
#
#     return render(request,'owner/show_report.html',{'subjects':subjects})

def show_report(request):
    if 'username_admin' in request.session:

        if request.method == 'POST':
            Searchfield = request.POST['name']
            batches = Batches.objects.filter(Batch_Name__icontains=Searchfield) | Batches.objects.filter(
                Month__icontains=Searchfield) | Batches.objects.filter(Year__icontains=Searchfield)
            return render(request, 'owner/show_report.html', {'batches': batches})

        else:
            batches = Batches.objects.all()
            batches = reversed(batches)
            return render(request, 'owner/show_report.html', {'batches': batches})

    else:
        return redirect('/owner/adminlogin')


def report(request, batch_id):
    global total_attendance
    if 'username_admin' in request.session:
        # Latest_Batch = Batches.objects.all().order_by('-id').first()
        batch = Batches.objects.get(id=batch_id)
        candidates = Candidates.objects.filter(ApplicationId__Batch=batch)
        marks = Marks.objects.all()
        return render(request, 'owner/report.html',
                      {'marks': marks, 'users': candidates, 'batch': batch, 'total_attendance': total_attendance})

    else:
        return redirect('/owner/adminlogin')


def report_download(request, batch_id):
    global total_attendance
    if 'username_admin' in request.session:
        batch = Batches.objects.get(id=batch_id)
        candidates = Candidates.objects.filter(ApplicationId__Batch=batch)
        marks = Marks.objects.all()
        template_path = 'owner/pdf_report.html'
        context = {'marks': marks, 'users': candidates}
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
    else:
        return redirect('/owner/adminlogin')


def report_mark(request, batch_id):
    global total_attendance
    if 'username_admin' in request.session:
        batch = Batches.objects.get(id=batch_id)
        candidates = Candidates.objects.filter(ApplicationId__Batch=batch)
        marks = Marks.objects.all()
        return render(request, 'owner/report_mark.html',
                      {'marks': marks, 'users': candidates, 'batch': batch, 'total_attendance': total_attendance})

    else:
        return redirect('/owner/adminlogin')


def report_mark_download(request, batch_id):
    global total_attendance
    if 'username_admin' in request.session:
        batch = Batches.objects.get(id=batch_id)
        candidates = Candidates.objects.filter(ApplicationId__Batch=batch)
        marks = Marks.objects.all()

        template_path = 'owner/pdf_report_mark.html'
        context = {'marks': marks, 'users': candidates, 'total_attendance': total_attendance}
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
    else:
        return redirect('/owner/adminlogin')


def report_attendance(request, batch_id):
    global total_attendance
    if 'username_admin' in request.session:
        batch = Batches.objects.get(id=batch_id)
        candidates = Candidates.objects.filter(ApplicationId__Batch=batch)
        marks = Marks.objects.all()
        return render(request, 'owner/report_attendance.html',
                      {'marks': marks, 'users': candidates, 'batch': batch, 'total_attendance': total_attendance})

    else:
        return redirect('/owner/adminlogin')


def report_attendance_download(request, batch_id):
    global total_attendance
    if 'username_admin' in request.session:
        batch = Batches.objects.get(id=batch_id)
        candidates = Candidates.objects.filter(ApplicationId__Batch=batch)
        marks = Marks.objects.all()

        template_path = 'owner/pdf_report_attendance.html'
        context = {'marks': marks, 'users': candidates, 'total_attendance': total_attendance}
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
    else:
        return redirect('/owner/adminlogin')


# User edit Edited by Devaprasad

def user_edit(request, batch_id):
    if 'username_admin' in request.session:
        if request.method == 'POST':

            Searchfield = request.POST['name']
            users = Candidates.objects.filter(ApplicationId__Phd_Reg__contains=Searchfield) | Candidates.objects.filter(
                ApplicationId__Name__icontains=Searchfield)

            return render(request, 'owner/user_edit.html', {'users': users, 'message': 'User not found'})
        else:
            batch = Batches.objects.get(id=batch_id)
            users = Candidates.objects.filter(ApplicationId__Batch=batch)

            return render(request, 'owner/user_edit.html', {'users': users, 'message': 'User not found'})

    else:
        return redirect('/owner/adminlogin')


def edit_form(request, userid):
    if 'username_admin' in request.session:
        user_det = Candidates.objects.get(Register_Number=userid)

        if request.method == 'POST':
            Name = request.POST['Name']
            Email = request.POST['Email']
            Mob = request.POST['Mob']
            Dob = request.POST['Dob']
            Gender = request.POST['Gender']
            Address = request.POST['Address']
            Phd_Reg = request.POST['Phd_Reg']
            Phd_Joining_Date = request.POST['Phd_Joining_Date']
            Research_Topic = request.POST['Research_Topic']
            Research_Guide = request.POST['Research_Guide']
            Guide_Mail = request.POST['Guide_Mail']
            Guide_Phone = request.POST['Guide_Phone']
            Drop_Out = request.POST['Drop_Out']

            user_det.ApplicationId.Name = Name
            user_det.ApplicationId.Email = Email
            user_det.ApplicationId.Mob = Mob
            user_det.ApplicationId.Dob = Dob
            user_det.ApplicationId.Gender = Gender
            user_det.ApplicationId.Address = Address
            user_det.ApplicationId.Phd_Reg = Phd_Reg
            user_det.ApplicationId.Phd_Joining_Date = Phd_Joining_Date
            user_det.ApplicationId.Research_Topic = Research_Topic
            user_det.ApplicationId.Research_Guide = Research_Guide
            user_det.ApplicationId.Guide_Mail = Guide_Mail
            user_det.ApplicationId.Guide_Phone = Guide_Phone
            user_det.Dropout = Drop_Out

            user_det.save()
            user_det.ApplicationId.save()

            return redirect(f'/owner/user_edit/{user_det.ApplicationId.Batch.id}')

        else:
            return render(request, 'owner/edit_form.html', {'person_details': user_det})

    else:
        return redirect('/owner/adminlogin')


# Payment section coded by Devaprasad


def payment_edit(request):
    if 'username_admin' in request.session:
        if request.method == 'POST':
            Paymentname = request.POST['paymentname']
            FreeForCusat = request.POST['Cusatian']

            Payment = Payments()
            Payment.PaymentName = Paymentname
            Payment.FreeForCusat = FreeForCusat

            Payment.save()

            # subjects = Subjects.objects.all().order_by('id')

            return redirect('/owner/payment_edit')
        else:
            payments = Payments.objects.all().order_by('id')
            return render(request, 'owner/payment.html', {'payments': payments})
    else:
        return redirect('/owner/adminlogin')


def payment_update(request, paymentid):
    if 'username_admin' in request.session:
        if request.method == 'POST':
            Paymentname = request.POST['paymentname']
            FreeForCusat = request.POST['Cusatian']

            Payment = Payments.objects.get(id=paymentid)

            Payment.PaymentName = Paymentname
            Payment.FreeForCusat = FreeForCusat

            Payment.save()

            return redirect(f'/owner/payment_update/{Payment.id}')
        else:

            payments = Payments.objects.all().order_by('id')
            return render(request, 'owner/payment.html',
                          {'payments': payments, 'message': f" payment details updated successfully"})

    else:
        return redirect('/owner/adminlogin')


def payment_delete(request, paymentid):
    if 'username_admin' in request.session:
        Payment = Payments.objects.get(id=paymentid)

        Payment.delete()
        return redirect(f"/owner/payment_edit")
    else:
        return redirect('/owner/adminlogin')


def payment_show_subjects(request):
    if 'username_admin' in request.session:
        subjects = Subjects.objects.all().order_by('id')
        if request.method == 'POST':
            Searchfield = request.POST['name']

            subjects = Subjects.objects.filter(SubjectName__icontains=Searchfield)
            return render(request, 'owner/show_subjects_payment.html', {'subjects': subjects})

        else:

            subjects = Subjects.objects.all().order_by('id')
            return render(request, 'owner/show_subjects_payment.html', {'subjects': subjects})
    else:
        return redirect('/owner/adminlogin')
