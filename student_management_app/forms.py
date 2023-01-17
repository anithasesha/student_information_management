from django import forms 
from django.forms import Form
from django.forms import formset_factory
from .models import StudentMarks, StudentDetails
from django.forms import ModelForm

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
