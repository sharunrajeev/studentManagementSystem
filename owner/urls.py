# from django.contrib import admin
from django.urls import path

from user.views import dashboard
from . import views

urlpatterns = [

    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('logout',views.logout,name='logout'),
    # Home page
    # path('', views.dashboard, name='dashboard'),
    path('approve', views.approve, name='approve'),
    path('approve/<userid>', views.individual_view, name='individual_view'),
    path('payment_subject',views.payment_subject,name='payment_subject'),
    #Done By Akhila

    path('payment/<userid>', views.user_verify_view, name='user_verify_view' ),
    path('denial/<userid>', views.denial, name='denial'),
    path('verified/<userid>', views.verified, name='verified'),
    path('reject/<userid>', views.reject, name='reject'),
    path('select/<userid>', views.select, name='select'),
    
    # User management path
    path('user_manage', views.user_manage, name='user_manage'),
    path('search_user', views.search_user, name='search_user'),
    path('view_user/<email>', views.view_user, name='view_user'),
    path('update_user/<email>', views.update_user, name='update_user'),
    path('delete_user/<userid>', views.delete_user, name='delete_user'),

    # Mark Uploading Coded By Devaprasad
    path('show_students', views.show_students, name='show_students'),
    path('mark_upload/<userid>', views.individual_mark_upload, name='individual_mark_upload'),
    path('mark_edit/<userid>', views.mark_edit, name='mark_edit'),
    path('mark_edit/mark_update/<markid>', views.mark_update, name='mark_update'),
    path('mark_edit/mark_delete/<markid>', views.mark_delete, name='mark_update'),
    path('show_report', views.show_report, name='show_report'),
    path('report', views.report, name='report'),
    path('report_download', views.report_download, name='report_download'),
    path('report_mark', views.report_mark, name='report_mark'),
    path('report_mark_download', views.report_mark_download, name='report_mark_download'),
    path('report_attendance', views.report_attendance, name='report_attendance'),
    path('report_attendance_download', views.report_attendance_download, name='report_attendance_download'),
    #Subject Adding Coded By Hana

    path('subjects_edit',views.subjects_edit,name='subjects_edit'),
    # path('subject_delete/<subjectid>',views.subject_delete,name='subject_delete'),
    path('subject_update/<subjectid>',views.subject_update,name='subject_update'),

    #coded by dp
    path('show_batches',views.show_batches,name='show_batches'),
    path('user_edit/<batch_id>' , views.user_edit , name = 'user_edit'),
    path('edit_form/<userid>' , views.edit_form , name = 'edit_form'),

    # payment section
    path('payment_edit', views.payment_edit, name='payment_edit'),
    path('payment_update/<paymentid>', views.payment_update, name='payment_update'),
    path('payment_delete/<paymentid>',views.payment_delete,name="payment_delete"),
    path('payment_show_subjects', views.payment_show_subjects, name='payment_show_subjects'),
]

