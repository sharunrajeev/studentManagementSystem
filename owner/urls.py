# from django.contrib import admin
from django.urls import path

from user.views import dashboard
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('approve', views.approve, name='approve'),
    path('reject/<userid>', views.reject, name='reject'),
    path('select/<userid>', views.select, name='select'),
    path('user_manage', views.user_manage, name='user_manage'),
    path('search_user', views.search_user, name='search_user'),
]
