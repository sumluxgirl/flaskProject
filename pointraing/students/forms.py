from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class StudentActivityForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    sub_type_id = SelectField('Тип')
    file = FileField('Загрузите грамоту/сертификат', validators=[FileAllowed(['jpg', 'png', 'pdf']), FileRequired()])
    submit = SubmitField('Отправить')
