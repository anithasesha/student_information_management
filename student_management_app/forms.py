from django import forms 
from django.forms import Form
from django.forms import formset_factory
from .models import StudentMarks, StudentDetails
from django.forms import ModelForm
import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
import django_filters
from django_tables2 import Column
from django.utils.safestring import mark_safe

class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(),
            'date_of_joining': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class EditStudentForm(forms.ModelForm):
    class Meta:
        model = StudentDetails
        exclude = ('register_number',)        
        widgets = {
            'date_of_birth': DateInput(),
            'date_of_joining': DateInput(),
        }

    field_order = ['student_photo']

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class StudentLinkColumn(Column):
    def render(self, value, record):
        return mark_safe(f'<a href="/edit_student/{record.register_number}">{value}</a>')


class ImageColumn(Column):

    def render(self, value, record):
        return mark_safe(f'<img src="{record.student_photo}" style="width: 50px;" />')

class StudentDetailsTable(tables.Table):
    name = StudentLinkColumn()
    student_photo = ImageColumn()
    class Meta:
        model = StudentDetails
        fields = ('student_photo','register_number','name','gender','course','mail_id','caste',)
        template_name = 'django_tables2/bootstrap.html'


class StudentDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = StudentDetails
        fields = ['register_number', 'name', 'caste']
