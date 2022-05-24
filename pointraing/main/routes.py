from flask import render_template, url_for, redirect, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role.name == 'Студент':
        return redirect(url_for('student_education'))
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')
