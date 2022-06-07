# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('approve', views.approve,name='approve'),
    path('delete/<userid>',views.delete,name='delete'),
    path('select/<userid>',views.select,name='select')

]