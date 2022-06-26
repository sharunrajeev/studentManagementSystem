from django.contrib import admin
from .models import Applicants,Candidates,Marks,Subjects,Payments,UserPayments
# Register your models here.

admin.site.register(Applicants)
admin.site.register(Candidates)
admin.site.register(Marks)
admin.site.register(Subjects)
admin.site.register(Payments)
admin.site.register(UserPayments)


