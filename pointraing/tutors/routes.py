from flask import Blueprint, render_template, redirect, flash
from flask_login import login_required
from pointraing.models import Subject, Attendance, User, Group, AttendanceGrade
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

tutors = Blueprint('tutors', __name__, template_folder='templates', url_prefix='/tutors')


@tutors.route("/subjects")
@login_required
def subjects():
    subjects_list = Subject.query.all()
    return render_template('subjects.html',
                           title="Учебные предметы",
                           subjects=subjects_list
                           )


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
        flash('Выбранной группы не существует, обратитесь к администратору системы', 'warning')
        return redirect('main.home')
    students_list = current_group.users.order_by(User.surname).all()
    attendance = current_group.attendance \
        .with_entities(Attendance.id, Attendance.date) \
        .filter(Attendance.subject_id == subject_id).order_by(Attendance.date)

    students = []
    attendance_sq = Attendance.query.with_entities(Attendance.id) \
        .filter(Attendance.subject_id == subject_id) \
        .filter(Attendance.group_id == group_id)
    for item in students_list:
        student = {
            'id': item.id,
            'name': ' '.join([item.surname, item.name, item.patronymic])
        }
        attendance_grade = AttendanceGrade.query \
            .filter(AttendanceGrade.user_id == item.id) \
            .filter(AttendanceGrade.attendance_id.in_(attendance_sq)).all()
        for att_item in attendance_grade:
            student.update({
                att_item.attendance_id: {
                    'id': att_item.id,
                    'active': att_item.active
                }
            })
        students.append(student)

    return {
        'groups': groups,
        'current_group': current_group,
        'students': students,
        'attendance': attendance
    }


@tutors.route("/subjects/<string:subject_id>")
@tutors.route("/subjects/<string:subject_id>/groups/<string:group_id>")
@login_required
def get_attendance(subject_id, group_id=None):
    lists = get_groups(subject_id, group_id)
    current_group = lists['current_group']
    if not group_id:
        group_id = current_group.id

    return render_template('attendance.html',
                           title="Посещение предмета",
                           groups=lists['groups'],
                           subject_id=subject_id,
                           group_id=group_id,
                           students=lists['students'],
                           attendance=lists['attendance']
                           )


@tutors.route("/subjects/<string:subject_id>/attendance/<string:attendance_id>/update")
@tutors.route("/subjects/<string:subject_id>/groups/<string:group_id>/attendance/<string:attendance_id>/update")
@login_required
def attendance_grade_update(subject_id, attendance_id, group_id=None):
    lists = get_groups(subject_id, group_id)
    if not group_id:
        current_group = lists['current_group']
        group_id = current_group.id

    class AttendanceGradeForm(FlaskForm):
        pass
    AttendanceGradeForm.submit = SubmitField('Сохранить')

    students = lists['students']
    choices = [
        (1, 'Присутсвует'),
        (2, 'Отсутсвует'),
        (3, 'Активность')
    ]
    for item in students:
        field_name = '_'.join(item['id'], item[attendance_id]['id']) if attendance_id in item else item['id']
        setattr(AttendanceGradeForm, field_name, SelectField(field_name, choices=choices))

    form = AttendanceGradeForm()
    return render_template('attendance_update.html',
                           title="Посещение предмета",
                           groups=lists['groups'],
                           subject_id=subject_id,
                           group_id=group_id,
                           attendance_id=attendance_id,
                           students=students,
                           attendance=lists['attendance'],
                           form=form
                           )
