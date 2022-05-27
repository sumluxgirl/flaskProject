from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required
from pointraing.models import Subject, Attendance, User, Group, AttendanceGrade

tutors = Blueprint('tutors', __name__, template_folder='templates', url_prefix='/tutors')


@tutors.route("/subjects")
@login_required
def subjects():
    subjects_list = Subject.query.all()
    return render_template('subjects.html',
                           title="Учебные предметы",
                           subjects=subjects_list
                           )


@tutors.route("/subjects/<string:subject_id>")
@tutors.route("/subjects/<string:subject_id>/groups/<string:group_id>")
@login_required
def get_groups(subject_id, group_id=None):
    groups = []
    for attendance in Attendance.query.filter(Attendance.subject_id == subject_id).group_by(Attendance.group_id):
        groups.append(attendance.group)
    if not group_id and len(groups) > 0:
        group_id = groups[0].id
    if not group_id:
        flash('Данные по группам не заполнены, обратитесь к администратору системы', 'warning')
        return redirect('main.home')
    current_group = Group.query.get_or_404(group_id)
    if not current_group:
        flash('Выбранной группы не существсует, обратитесь к администратору системы', 'warning')
        return redirect('main.home')
    students_list = current_group.users.order_by(User.surname).all()
    students = []
    attendance = current_group.attendance \
        .with_entities(Attendance.id, Attendance.date) \
        .filter(Attendance.subject_id == subject_id).order_by(Attendance.date)
    attendance_sq = Attendance.query.with_entities(Attendance.id)\
        .filter(Attendance.subject_id == subject_id)\
        .filter(Attendance.group_id == group_id)
    for item in students_list:
        student = {
            'name': ' '.join([item.surname, item.name, item.patronymic])
        }
        attendance_grade = AttendanceGrade.query\
            .filter(AttendanceGrade.user_id == item.id) \
            .filter(AttendanceGrade.attendance_id.in_(attendance_sq)).all()
        for att_item in attendance_grade:
            student.update({
                att_item.attendance_id: {
                    'active': att_item.active
                }
            })
        students.append(student)
    return render_template('groups.html',
                           title="Учебные предметы",
                           groups=groups,
                           subject_id=subject_id,
                           group_id=group_id,
                           students=students,
                           attendance=attendance
                           )
