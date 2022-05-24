from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required
from pointraing.models import Subject, Attendance, User

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
    students = User.query.filter(User.group_id == group_id).order_by(User.name).all()
    return render_template('groups.html',
                           title="Учебные предметы",
                           groups=groups,
                           subject_id=subject_id,
                           group_id=group_id,
                           students=students
                           )
