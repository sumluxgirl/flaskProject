from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

IS_EXIST = 1
NOT_EXIST = 2
ACTIVE = 3

CHOICES = [
    (IS_EXIST, 'Присутсвует'),
    (NOT_EXIST, 'Отсутсвует'),
    (ACTIVE, 'Активность')
]

CHOICES_GRADE_EXAM = [
    (0, '-'),
    (2, 'Неудовлетворительно'),
    (3, 'Удовлетворительно'),
    (4, 'Хорошо'),
    (5, 'Отлично')
]

CHOICES_GRADE_OFFSET = [
    (0, 'Не сдано'),
    (1, 'Сдано')
]


class AttendanceGradeForm(FlaskForm):
    submit = SubmitField('Сохранить')


class GradeUserForm(FlaskForm):
    grades_point = SelectField('Оценка', coerce=int)


class LabUserForm(FlaskForm):
    labs_point = SelectField('Оценка', coerce=int)
