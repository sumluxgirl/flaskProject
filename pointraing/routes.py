from pointraing import app, bcrypt
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from pointraing.forms import LoginForm
from pointraing.models import User


@app.route("/")
@app.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check login and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
