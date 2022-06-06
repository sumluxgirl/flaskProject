from flask import render_template, url_for, redirect, Blueprint, send_from_directory, current_app
from flask_login import current_user

main = Blueprint('main', __name__, template_folder='templates')


def get_full_name(item):
    return ' '.join([item.surname, item.name, item.patronymic])


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if current_user.role.name == 'Студент':
        return redirect(url_for('students.education'))
    elif current_user.role.name == 'Преподаватель':
        return redirect(url_for('tutors.subjects'))
    elif current_user.role.name == 'Деканат':
        return redirect(url_for('deans_office.rating'))
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], name)
