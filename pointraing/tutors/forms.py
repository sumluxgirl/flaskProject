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


class AttendanceGradeForm(FlaskForm):
    submit = SubmitField('Сохранить')


class GradeUserForm(FlaskForm):
    grades_point = SelectField('Оценка', choices=[
        (2, 'Неудовлетворительно'),
        (3, 'Удовлетворительно'),
        (4, 'Хорошо'),
        (5, 'Отлично')
    ], coerce=int)
