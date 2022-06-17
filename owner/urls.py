# from django.contrib import admin
from django.urls import path

from user.views import dashboard
from . import views

urlpatterns = [

    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('logout',views.logout,name='logout'),
    # Home page
    path('', views.dashboard, name='dashboard'),
    path('approve', views.approve, name='approve'),
    path('approve/<userid>', views.individual_view, name='individual_view'),
    path('payment',views.payment,name='payment'),
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
    path('mark_upload', views.mark_upload, name='mark_upload'),
    path('mark_upload/<userid>', views.individual_mark_upload, name='individual_mark_upload'),
    path('mark_edit/<userid>', views.mark_edit, name='mark_edit'),
    path('mark_edit/mark_update/<markid>', views.mark_update, name='mark_update'),
    path('mark_edit/mark_delete/<markid>', views.mark_delete, name='mark_update'),
    path('show_report', views.show_report, name='show_report'),
    path('report/<subjectid>', views.report, name='report'),
    path('report/report_download/<subjectid>', views.report_download, name='report_download'),
    path('report_mark', views.report_mark, name='report_mark'),
    path('report_attendance', views.report_attendance, name='report_attendance'),
    #Subject Adding Coded By Hana

    path('subjects_edit',views.subjects_edit,name='subjects_edit'),
    path('subject_delete/<subjectid>',views.subject_delete,name='subject_delete'),
    path('subject_update/<subjectid>',views.subject_update,name='subject_update')
]

