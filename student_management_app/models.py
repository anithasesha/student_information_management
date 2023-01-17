from html import escape
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class StudentDetails(models.Model):
    id = models.AutoField(primary_key=True)
    register_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=50, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=100)
    nationality = models.CharField(max_length=150)
    caste = models.CharField(max_length=150)
    community = models.CharField(max_length=150)
    religion = models.CharField(max_length=150)
    mail_id = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    aadhar_number = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    date_of_joining = models.DateField()
    course = models.CharField(max_length=250)
    student_photo = models.ImageField()
    family_photo = models.ImageField()
    father_name = models.CharField(max_length=250)
    mother_name = models.CharField(max_length=250)
    father_occupation = models.CharField(max_length=250)
    mother_occupation = models.CharField(max_length=250)
    parent_phone_number = models.CharField(max_length=20)
    parent_annual_income = models.IntegerField()
    bank_name = models.CharField(max_length=250)
    bank_account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    objects = models.Manager()


class StudentMarks(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(StudentDetails, on_delete=models.CASCADE)
    semester = models.IntegerField()
    language_subject_code = models.CharField(max_length=20,null=True,blank=True)
    language_marks = models.FloatField(null=True,blank=True)
    english_subject_code = models.CharField(max_length=20,null=True,blank=True)
    english_marks = models.FloatField(null=True,blank=True)
    major_subject_code = models.CharField(max_length=20,null=True,blank=True)
    major_marks = models.FloatField(null=True,blank=True)
    allied_subject_code = models.CharField(max_length=20,null=True,blank=True)
    allied_marks = models.FloatField(null=True,blank=True)
    elective_subject_code = models.CharField(max_length=20,null=True,blank=True)
    elective_marks = models.FloatField(null=True,blank=True)
    major_practical_subject_code = models.CharField(max_length=20,null=True,blank=True)
    major_practical_marks = models.FloatField(null=True,blank=True)
    allied_practical_subject_code = models.CharField(max_length=20,null=True,blank=True)
    allied_practical_marks = models.FloatField(null=True,blank=True)
    objects = models.Manager()
