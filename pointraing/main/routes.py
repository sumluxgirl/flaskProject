from flask import render_template, url_for, redirect, Blueprint, send_from_directory, current_app
from flask_login import current_user
from pointraing.models import AttendanceGrade, Attendance, LabsGrade, Lab, GradeUsers, Grade, TypeGrade, User, Subject

main = Blueprint('main', __name__, template_folder='templates')


def get_full_name(item):
    return ' '.join([item.surname, item.name, item.patronymic])


def get_education_student_by_subject(student_id, subject_id):
    student = User.query.get_or_404(student_id)
    attendance_user = AttendanceGrade.query \
        .filter(AttendanceGrade.user_id == student.id).subquery()
    attendance = Attendance.query \
        .filter(Attendance.subject_id == subject_id) \
        .filter(Attendance.group_id == student.group_id) \
        .add_columns(attendance_user.c.id, attendance_user.c.active) \
        .outerjoin(attendance_user, Attendance.id == attendance_user.c.attendance_id) \
        .order_by(Attendance.date).all()
    attendance_count_user = AttendanceGrade.query \
        .join(AttendanceGrade.attendance) \
        .filter(Attendance.subject_id == subject_id) \
        .filter(AttendanceGrade.user_id == student.id) \
        .count()
    labs_user_subq = LabsGrade.query \
        .filter(LabsGrade.user_id == student.id).subquery()
    labs = Lab.query \
        .filter(Lab.subject_id == subject_id) \
        .add_columns(labs_user_subq.c.id, labs_user_subq.c.date) \
        .outerjoin(labs_user_subq, Lab.id == labs_user_subq.c.lab_id) \
        .all()
    labs_count_user = LabsGrade.query \
        .join(Lab, LabsGrade.lab) \
        .filter(Lab.subject_id == subject_id) \
        .filter(LabsGrade.user_id == student.id) \
        .count()
    grade = GradeUsers.query \
        .join(GradeUsers.grade) \
        .join(Grade.type) \
        .with_entities(GradeUsers.value, TypeGrade.name, Grade.date) \
        .filter(GradeUsers.user_id == student.id) \
        .filter(Grade.subject_id == subject_id) \
        .group_by(GradeUsers.id) \
        .all()

    return attendance_count_user, len(attendance), attendance, labs_count_user, len(labs), labs, grade


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
