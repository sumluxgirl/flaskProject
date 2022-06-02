from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required
from pointraing.models import Subject, Attendance, User, Group, AttendanceGrade
from pointraing import db
from wtforms import SelectField
from datetime import datetime
from pointraing.tutors.forms import AttendanceGradeForm, CHOICES, IS_EXIST, NOT_EXIST, ACTIVE
import uuid
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


@tutors.route("/subjects/<string:subject_id>/attendance/<string:attendance_id>/update", methods=['GET', 'POST'])
@tutors.route("/subjects/<string:subject_id>/groups/<string:group_id>/attendance/<string:attendance_id>/update",
              methods=['GET', 'POST'])
@login_required
def attendance_grade_update(subject_id, attendance_id, group_id=None):
    current_attendance = Attendance.query.get_or_404(attendance_id)
    is_new = (current_attendance.date - datetime.now()).total_seconds() >= 0
    if not current_attendance:
        flash('Такого посещения нет, обратитесь к администратору системы', 'warning')
        return redirect('main.home')
    lists = get_groups(subject_id, group_id)
    if not group_id:
        current_group = lists['current_group']
        group_id = current_group.id

    students = lists['students']
    list_sorter = {}
    for item in students:
        field_name = item['id']
        if attendance_id in item:
            list_sorter.update({
                item['id']: item[attendance_id]
            })
        setattr(AttendanceGradeForm, field_name, SelectField(field_name, choices=CHOICES, coerce=int))

    form = AttendanceGradeForm()

    if form.validate_on_submit():
        attendances_grade = []
        for item in students:
            student_id = item['id']
            if form[student_id].data in (IS_EXIST, ACTIVE):
                if is_new or student_id not in list_sorter:
                    attendances_grade.append(AttendanceGrade(
                        id=uuid.uuid4().hex,
                        user_id=student_id,
                        attendance_id=attendance_id,
                        active=1 if form[student_id].data == ACTIVE else 0
                    ))
                else:
                    attendance_grade = AttendanceGrade.query.get_or_404(list_sorter[student_id]['id'])
                    attendance_grade.active = 1 if form[student_id].data == ACTIVE else 0
            else:
                if student_id in list_sorter:
                    attendance_grade = AttendanceGrade.query.get_or_404(list_sorter[student_id]['id'])
                    db.session.delete(attendance_grade)
        if len(attendances_grade) > 0:
            db.session.add_all(attendances_grade)
        db.session.commit()
        flash('Посещение обновлено!', 'success')
        return redirect(url_for('tutors.get_attendance', subject_id=subject_id, group_id=group_id))
    elif request.method == 'GET':
        if not is_new:
            for item in students:
                student_id = item['id']
                if student_id in list_sorter:
                    form[student_id].data = (ACTIVE if list_sorter[student_id]['active'] else IS_EXIST)
                else:
                    form[student_id].data = NOT_EXIST

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
