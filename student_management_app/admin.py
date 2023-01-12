from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentDetails, StudentMarks

admin.site.register(StudentDetails)
admin.site.register(StudentMarks)
