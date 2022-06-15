from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired


class DeclineActivityForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class SubjectForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    count_hours = IntegerField('Количество часов', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class LabForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    subject = SelectField('Предмет', validators=[DataRequired()])
    datetime = DateTimeLocalField('Дата', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    deadline = DateTimeLocalField('Дедлайн', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Сохранить')


class AttendanceForm(FlaskForm):
    subject = SelectField('Предмет', validators=[DataRequired()])
    group = SelectField('Группа', validators=[DataRequired()])
    type = SelectField('Тип', validators=[DataRequired()])
    date = DateTimeLocalField('Дата', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Сохранить')


class SimpleEntityForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class GradeForm(FlaskForm):
    subject = SelectField('Предмет', validators=[DataRequired()])
    type = SelectField('Тип', validators=[DataRequired()])
    date = DateTimeLocalField('Дата', validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Сохранить')
