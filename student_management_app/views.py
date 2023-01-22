from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from student_management_app.models import StudentDetails, StudentMarks
from .forms import AddStudentForm, EditStudentForm, StudentDetailsTable, StudentDetailsFilter
from django.forms import modelformset_factory,modelform_factory, inlineformset_factory
from django.shortcuts import render
from django_tables2 import RequestConfig
from django_filters.views import FilterView


def home(request):
    students = StudentDetails.objects.all()
    context = {
        "students": students
    }
    # return render(request, 'home_template.html', context)
    table = StudentDetailsTable(StudentDetails.objects.all())
    RequestConfig(request).configure(table)
    context = {
        'table': table,
    }
    return render(request, 'mytemplate.html', context)



# class StudentDetailsFilterView(FilterView):
#     filterset_class = StudentDetailsFilter
#     template_name = 'mytemplate.html'
#     table_class = StudentDetails

#     def get(self, request, *args, **kwargs):
#         self.table = self.table_class(self.filterset.qs)
#         RequestConfig(request, paginate={'per_page': 20}).configure(self.table)
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['table'] = self.table
#         return context

class StudentDetailsFilterView(FilterView):
    filterset_class = StudentDetailsFilter
    template_name = 'mytemplate.html'
    table_class = StudentDetailsTable
    queryset = StudentDetails.objects.all()
    # model = StudentDetails

    # def get_queryset(self):
    #     return StudentDetails.objects.filter(self.request.GET)

    def get(self, request, *args, **kwargs):
        self.table = self.table_class(self.get_queryset())
        # self.table = self.table_class(self.filterset.qs)
        RequestConfig(request, paginate={'per_page': 20}).configure(self.table)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.table
        return context


# class StudentDetailsFilterView(FilterView):
#     filterset_class = StudentDetailsFilter
#     template_name = 'mytemplate.html'


def add_student(request):
    form = AddStudentForm()
    
    studentMarksFormset = modelformset_factory(StudentMarks,exclude=('id','student_id',),extra=6, can_delete=False)
    markformset = studentMarksFormset(queryset=StudentMarks.objects.none(),initial=[{'semester': 1},{'semester': 2},{'semester': 3},{'semester': 4},{'semester': 5},{'semester': 6}])
    
    context = {
        "form": form,
        "formset": markformset
    }
    return render(request, 'add_student_template.html', context)


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) != 0:
                student_photo = request.FILES['student_photo']
                fs = FileSystemStorage()
                filename = fs.save(student_photo.name, student_photo)
                form.cleaned_data['student_photo'] = fs.url(filename)

                family_photo = request.FILES['family_photo']
                fs = FileSystemStorage()
                filename = fs.save(family_photo.name, family_photo)
                form.cleaned_data['family_photo'] = fs.url(filename)

            try:
                student = StudentDetails.objects.create(
                    register_number = form.cleaned_data['register_number'],
                    name = form.cleaned_data['name'],
                    gender = form.cleaned_data['gender'],
                    date_of_birth = form.cleaned_data['date_of_birth'],
                    blood_group = form.cleaned_data['blood_group'],
                    nationality = form.cleaned_data['nationality'],
                    caste = form.cleaned_data['caste'],
                    community = form.cleaned_data['community'],
                    religion = form.cleaned_data['religion'],
                    mail_id = form.cleaned_data['mail_id'],
                    phone_number = form.cleaned_data['phone_number'],
                    aadhar_number = form.cleaned_data['aadhar_number'],
                    address = form.cleaned_data['address'],
                    date_of_joining = form.cleaned_data['date_of_joining'],
                    course = form.cleaned_data['course'],
                    student_photo = form.cleaned_data['student_photo'],
                    father_name = form.cleaned_data['father_name'],
                    mother_name = form.cleaned_data['mother_name'],
                    father_occupation = form.cleaned_data['mother_name'],
                    mother_occupation = form.cleaned_data['mother_occupation'],
                    parent_phone_number = form.cleaned_data['parent_phone_number'],
                    parent_annual_income = form.cleaned_data['parent_annual_income'],
                    family_photo = form.cleaned_data['family_photo'],
                    bank_name = form.cleaned_data['bank_name'],
                    bank_account_number = form.cleaned_data['bank_account_number'],
                    ifsc_code = form.cleaned_data['ifsc_code']
                )

                studentMarksFormset = modelformset_factory(StudentMarks,exclude=('id','student_id',), can_delete=False)
                if request.method == 'POST':
                    formset = studentMarksFormset(request.POST)
                    if formset.is_valid():
                        instances = formset.save(commit=False)
                        for instance in instances:
                            instance.student_id = student
                            instance.save()

                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except Exception as e: 
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id
    student = StudentDetails.objects.get(register_number=student_id)
    form = modelform_factory(StudentDetails,exclude=('id',))

    form = EditStudentForm()
    form.fields['student_photo'].required = False
    form.fields['family_photo'].required = False

    form.fields['name'].initial = student.name
    form.fields['gender'].initial = student.gender
    form.fields['date_of_birth'].initial = student.date_of_birth
    form.fields['blood_group'].initial = student.blood_group
    form.fields['nationality'].initial = student.nationality
    form.fields['caste'].initial = student.caste
    form.fields['community'].initial = student.community
    form.fields['religion'].initial = student.religion
    form.fields['mail_id'].initial = student.mail_id
    form.fields['phone_number'].initial = student.phone_number
    form.fields['aadhar_number'].initial = student.aadhar_number
    form.fields['address'].initial = student.address
    form.fields['date_of_joining'].initial = student.date_of_joining
    form.fields['course'].initial = student.course
    form.fields['student_photo'].initial = student.student_photo
    form.fields['father_name'].initial = student.father_name
    form.fields['mother_name'].initial = student.mother_name
    form.fields['father_occupation'].initial = student.father_occupation
    form.fields['mother_occupation'].initial = student.mother_occupation
    form.fields['parent_phone_number'].initial = student.parent_phone_number
    form.fields['parent_annual_income'].initial = student.parent_annual_income
    form.fields['family_photo'].initial = student.family_photo
    form.fields['bank_name'].initial = student.bank_name
    form.fields['bank_account_number'].initial = student.bank_account_number
    form.fields['ifsc_code'].initial = student.ifsc_code

    studentMarksFormset = inlineformset_factory(StudentDetails, StudentMarks, exclude=('id','student_id',),extra=0, can_delete=False)
    marksFormset = studentMarksFormset(instance=student)

    context = {
        "id": student_id,
        "name": student.name,
        "form": form,
        "formset": marksFormset
    }
    return render(request, "edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/home')

        form = EditStudentForm(request.POST, request.FILES)
        form.fields['student_photo'].required = False
        form.fields['family_photo'].required = False
        student = StudentDetails.objects.get(register_number=student_id)

        if form.is_valid():
            file_list=[]
            for filename, file in request.FILES.items():
                file_list.append(filename)
                
            if 'student_photo' in file_list:
                student_photo = request.FILES['student_photo']
                fs = FileSystemStorage()
                filename = fs.save(student_photo.name, student_photo)
                form.cleaned_data['student_photo'] = fs.url(filename)
            else:
                form.cleaned_data['student_photo'] = student.student_photo

            if 'family_photo' in file_list:
                family_photo = request.FILES['family_photo']
                fs = FileSystemStorage()
                filename = fs.save(family_photo.name, family_photo)
                form.cleaned_data['family_photo'] = fs.url(filename)
            else:
                form.cleaned_data['family_photo'] = student.family_photo

            try:
                student = StudentDetails.objects.get(register_number=student_id)
                student.name = form.cleaned_data['name']
                student.gender = form.cleaned_data['gender']
                student.date_of_birth = form.cleaned_data['date_of_birth']
                student.blood_group = form.cleaned_data['blood_group']
                student.nationality = form.cleaned_data['nationality']
                student.caste = form.cleaned_data['caste']
                student.community = form.cleaned_data['community']
                student.religion = form.cleaned_data['religion']
                student.mail_id = form.cleaned_data['mail_id']
                student.phone_number = form.cleaned_data['phone_number']
                student.aadhar_number = form.cleaned_data['aadhar_number']
                student.address = form.cleaned_data['address']
                student.date_of_joining = form.cleaned_data['date_of_joining']
                student.course = form.cleaned_data['course']
                student.student_photo = form.cleaned_data['student_photo']
                student.father_name = form.cleaned_data['father_name']
                student.mother_name = form.cleaned_data['mother_name']
                student.father_occupation = form.cleaned_data['mother_name']
                student.mother_occupation = form.cleaned_data['mother_occupation']
                student.parent_phone_number = form.cleaned_data['parent_phone_number']
                student.parent_annual_income = form.cleaned_data['parent_annual_income']
                student.family_photo = form.cleaned_data['family_photo']
                student.bank_name = form.cleaned_data['bank_name']
                student.bank_account_number = form.cleaned_data['bank_account_number']
                student.ifsc_code = form.cleaned_data['ifsc_code']
                student.save()
                
                studentMarksFormset = inlineformset_factory(StudentDetails, StudentMarks, exclude=('id','student_id',),extra=0, can_delete=False)
                marksFormset = studentMarksFormset(request.POST, request.FILES, instance=student)
                if marksFormset.is_valid():
                    marksFormset.save()
                        
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except Exception as e: 
                messages.error(request, "Failed to Update Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = StudentDetails.objects.get(register_number=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('home')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('home')


def print_tc(request, student_id):
    student = StudentDetails.objects.get(register_number=student_id)
    dob=student.date_of_joining.strftime("%d/%m/%Y")
    dob_str = convert_date(dob)
    context = {
        "id": student_id,
        "studentDetails": student,
        "dob": dob,
        "doj": student.date_of_joining.strftime("%d/%m/%Y"),
        "dob_str": dob_str,
    }
    return render(request, "print_tc_template.html", context)



def convert_date(date_string):
    day, month, year = date_string.split('/')
    month = int(month)
    year = int(year)
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    month_name = month_names[month - 1]
    year_in_words = convert_number_to_words(year)
    day_string = convert_day_to_ordinal(day)
    date_string = f"{day_string} {month_name} {year_in_words}"

    return date_string

def convert_number_to_words(n):
    n = int(n)

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    special_tens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]

    if n < 10:
        return ones[n]
    elif n < 20:
        return special_tens[n - 10]
    elif n < 100:
        return tens[n // 10] + ('' if n % 10 == 0 else ' ' + ones[n % 10])
    elif n < 1000:
        return ones[n // 100] + ' Hundred' + '' + convert_number_to_words(n % 100)
    elif n < 1000000:
        return convert_number_to_words(n // 1000) + ' Thousand' + ('' if n % 1000 == 0 else ' ' + convert_number_to_words(n % 1000))
    else:
        return "Number too large"

def convert_day_to_ordinal(day):
    day = int(day)
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    ordinals = ["", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth", "Eighteenth", "Nineteenth", "Twentieth"]

    if day < 21:
        return ordinals[day]
    elif day < 100:
        return tens[day // 10] + ' ' +ordinals[day % 10]
    else:
        return "Invalid day"
