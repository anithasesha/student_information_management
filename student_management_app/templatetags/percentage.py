from django import template

register = template.Library()

@register.filter
def sem_percentage(value):
    marks = value.instance
    total=0
    i=0
    if marks.language_subject_code:
        total += marks.language_marks
        i+1
    if marks.english_subject_code:
        total += marks.english_marks
        i+1
    if marks.major_subject_code:
        total += marks.major_marks
        i+1
    if marks.allied_subject_code:
        total += marks.allied_marks
        i+1
    if marks.elective_subject_code:
        total += marks.elective_marks
        i+1
    if marks.major_practical_subject_code:
        total += marks.major_practical_marks
        i+1
    if marks.allied_practical_subject_code:
        total += marks.allied_practical_marks
        i+1

    percentage = None
    if i != 0:
        percentage = total/i

    return percentage