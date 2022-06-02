from flask_wtf import FlaskForm
from wtforms import SubmitField

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
