# from django.contrib import admin
from django.urls import path

from user.views import dashboard
from . import views

urlpatterns = [
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
]

