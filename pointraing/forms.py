from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Login',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Заменить пароль')


class StudentActivityForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    sub_type_id = SelectField('Тип')
    file = FileField('Загрузите грамоту/сертификат', validators=[FileAllowed(['jpg', 'png', 'pdf'], FileRequired())])
    submit = SubmitField('Отправить')
