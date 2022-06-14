from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class DeclineActivityForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class SubjectForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    count_hours = IntegerField('Количество часов', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
