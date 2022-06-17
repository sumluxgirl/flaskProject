from flask import render_template, url_for, redirect, Blueprint, send_from_directory, current_app
from flask_login import current_user, login_required
from pointraing.main.utils import is_student, is_tutor, is_deans_office, get_full_name, get_education_student_by_subject

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    if is_student():
        return redirect(url_for('students.education'))
    elif is_tutor():
        return redirect(url_for('tutors.subjects'))
    elif is_deans_office():
        return redirect(url_for('deans_office.rating'))
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], name)


@main.route('/rating/student/<string:student_id>/subject/<string:subject_id>')
@login_required
def students_rating_by_subject(student_id, subject_id):
    from pointraing.models import User, Subject
    student = User.query.get_or_404(student_id)
    subject = Subject.query.get_or_404(subject_id)
    full_name = get_full_name(student)
    subject_name = subject.name
    attendance_count_user, count_hours, attendance, labs_count_user, labs_count, labs, grade, auto_grade = \
        get_education_student_by_subject(student_id, subject_id)
    return render_template('rating_by_subject.html',
                           title='Рейтинг студента по предмету',
                           full_name=full_name,
                           subject_name=subject_name,
                           attendance_count_user=attendance_count_user,
                           count_hours=count_hours,
                           attendance=attendance,
                           labs_count_user=labs_count_user,
                           labs_count=labs_count,
                           labs=labs,
                           grade=grade,
                           auto_grade=auto_grade
                           )
