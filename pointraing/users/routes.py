from flask import render_template, url_for, redirect, Blueprint, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from pointraing import db, bcrypt
from pointraing.models import User
from pointraing.users.forms import LoginForm, ResetPasswordForm

users = Blueprint('users', __name__, template_folder='templates')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте логин и пароль', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    user_name_tuple = (current_user.surname, current_user.name, current_user.patronymic)
    full_name = ' '.join(user_name_tuple)
    role = current_user.role.name
    group = current_user.group
    group_name = group.name if group else None
    return render_template('account.html', title='Account', full_name=full_name, role=role, group_name=group_name)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Недействительный или просроченный токен', 'warning')
        return redirect(url_for('users.account'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Пароль был изменен', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
