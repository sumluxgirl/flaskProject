from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DeclineActivityForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')
