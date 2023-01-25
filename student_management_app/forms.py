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
from django.utils.html import format_html
from django.urls import reverse

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

class StudentDetailsTable(tables.Table):
    action = tables.Column(empty_values=())
    
    class Meta:
        model = StudentDetails
        fields = ('student_photo','register_number','name','gender','course','mail_id','caste',)
        template_name = 'django_tables2/bootstrap.html'
    
    def render_student_photo(self, value, record):
        return format_html('<img src="{}" style="width: 50px;" />', record.student_photo)
        
    def render_name(self, value, record):
        return format_html('<a href="{}">{}</a>', reverse('view_student', args=[record.register_number]), value)

    def render_action(self, value, record):
        return format_html('<a href="{}"><img src="/static/admin/img/edit.png" style="height: 25px;width: 25px;"></a><a href="{}"><img src="/static/admin/img/print.png" style="height: 25px;width: 25px;"></a><a href="{}"><img src="/static/admin/img/delete.png" style="height: 25px;width: 25px;"></a>', reverse('edit_student', args=[record.register_number]),reverse('print_tc', args=[record.register_number]),reverse('delete_student', args=[record.register_number]))

