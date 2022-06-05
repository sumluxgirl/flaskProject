from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required
from pointraing.models import Subject, Attendance, User, Group, AttendanceGrade, Lab, LabsGrade, Grade, GradeUsers
from pointraing import db
from wtforms import SelectField
from datetime import datetime
from pointraing.tutors.forms import AttendanceGradeForm, CHOICES, IS_EXIST, NOT_EXIST, ACTIVE
import uuid

tutors = Blueprint('tutors', __name__, template_folder='templates', url_prefix='/tutors',
                   static_folder='static')


@tutors.route("/subjects")
@login_required
def subjects():
    subjects_list = Subject.query.all()
    return render_template('subjects.html',
                           title="Учебные предметы",
                           subjects=subjects_list
                           )


def get_main_lists(subject_id, group_id=None):
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
    return (
        groups,
        current_group,
        students_list,
        group_id
    )


def get_full_name(item):
    return ' '.join([item.surname, item.name, item.patronymic])


def get_groups(subject_id, group_id=None):
    groups, current_group, students_list, group_id = get_main_lists(subject_id, group_id)
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
            'name': get_full_name(item)
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
                           attendance=lists['attendance'],
                           active_tab='attendance'
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
                           students=lists['students'],
                           attendance=lists['attendance'],
                           form=form,
                           active_tab='attendance'
                           )


@tutors.route("/subjects/<string:subject_id>/labs")
@tutors.route("/subjects/<string:subject_id>/groups/<string:group_id>/labs")
@login_required
def get_labs(subject_id, group_id=None):
    groups, current_group, students_list, group_id = get_main_lists(subject_id, group_id)
    students = []
    labs = Lab.query \
        .with_entities(Lab.id, Lab.deadline, Lab.name) \
        .filter(Lab.subject_id == subject_id).order_by(Lab.datetime)
    lab_sq = Lab.query.with_entities(Lab.id) \
        .filter(Attendance.subject_id == subject_id)
    for item in students_list:
        student = {
            'id': item.id,
            'name': get_full_name(item)
        }
        labs_grade = LabsGrade.query \
            .filter(LabsGrade.user_id == item.id) \
            .filter(LabsGrade.lab_id.in_(lab_sq)).all()
        for lab_item in labs_grade:
            student.update({
                lab_item.lab_id: {
                    'id': lab_item.id,
                    'date': lab_item.date
                }
            })
        students.append(student)
    return render_template('labs.html',
                           title="Лабораторные",
                           groups=groups,
                           subject_id=subject_id,
                           group_id=group_id,
                           students=students,
                           labs=labs,
                           active_tab='labs'
                           )


@tutors.route("/subjects/<string:subject_id>/grade")
@tutors.route("/subjects/<string:subject_id>/groups/<string:group_id>/grade")
@login_required
def get_grades(subject_id, group_id=None):
    groups, current_group, students_list, group_id = get_main_lists(subject_id, group_id)
    students = []
    grades = Grade.query \
        .filter(Grade.subject_id == subject_id).order_by(Grade.date)
    grades_sq = Grade.query.with_entities(Grade.id) \
        .filter(Grade.subject_id == subject_id)
    for item in students_list:
        student = {
            'id': item.id,
            'name': get_full_name(item)
        }
        grade_users = GradeUsers.query \
            .filter(GradeUsers.user_id == item.id) \
            .filter(GradeUsers.grade_id.in_(grades_sq)).all()
        for grade_item in grade_users:
            student.update({
                grade_item.grade_id: {
                    'id': grade_item.id,
                    'value': grade_item.value
                }
            })
        students.append(student)
    return render_template('grades.html',
                           title="Зачет/Экзамен",
                           groups=groups,
                           grades=grades,
                           students=students,
                           subject_id=subject_id,
                           group_id=group_id,
                           active_tab='grade'
                           )
