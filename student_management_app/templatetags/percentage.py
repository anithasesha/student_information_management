from django import template
from student_management_app.models import StudentDetails, StudentMarks

register = template.Library()

@register.filter
def sem_percentage(value):
    marks = value
    total=0
    i=0
    # if marks.language_subject_code:
    #     total += marks.language_marks
    #     i+=1
    # if marks.english_subject_code:
    #     total += marks.english_marks
    #     i+=1
    if marks.major_subject_code:
        total += marks.major_marks
        i+=1
    if marks.allied_subject_code:
        total += marks.allied_marks
        i+=1
    if marks.elective_subject_code:
        total += marks.elective_marks
        i+=1
    if marks.major_practical_subject_code:
        total += marks.major_practical_marks
        i+=1
    if marks.allied_practical_subject_code:
        total += marks.allied_practical_marks
        i+=1

    percentage = None
    if i != 0:
        percentage = total/i
        percentage = round(percentage,1)


    return percentage


@register.filter
def overall_percentage(id, semester):
    student = StudentDetails.objects.get(register_number=id)
    marks = StudentMarks.objects.filter(student_id=student.id)
    total_percent = 0
    i = 0
    current_sem_percent = sem_percentage(marks[semester-1])
    if current_sem_percent:
        for i in range(int(semester)):
            sem_percent = sem_percentage(marks[i])
            if sem_percent:
                total_percent += sem_percent
                i+=1

    overall_percent = None
    if i != 0:
        overall_percent = total_percent/i
        overall_percent = round(overall_percent,1)

    return overall_percent