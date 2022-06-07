from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from pointraing.models import Group, User, Subject, Attendance, Activity, Lab
from pointraing.main.routes import get_full_name
from pointraing import db
from pointraing.deans_office.forms import DeclineActivityForm

deans_office = Blueprint('deans_office', __name__, template_folder='templates')

SUBJECT = 'subject'
LAB = 'lab'
ATTENDANCE = 'attendance'
ATTENDANCE_TYPE = 'attendance_type'
GRADE = 'grade'
TYPE_GRADE = 'type_grade'
GROUP = 'group'
ROLE = 'role'
USER = 'user'
ACTIVITY_TYPE = 'activity_type'
ACTIVITY_SUB_TYPE = 'activity_sub_type'
RATE_ACTIVITY = 'rate_activity'


@deans_office.route('/rating')
@deans_office.route('/rating/group/<string:group_id>')
@deans_office.route('/rating/group/<string:group_id>/student/<string:student_id>')
@login_required
def rating(group_id=None, student_id=None):
    groups = Group.query.order_by(Group.name).all()
    if not group_id:
        if len(groups) > 0:
            current_group = groups[0]
            group_id = current_group.id
        else:
            flash('Групп пока не существует, обратитесь к администратору системы', 'warning')
            return redirect(url_for('main.home'))
    else:
        current_group = Group.query.get_or_404(group_id)
    students_list = current_group.users.all()
    if not student_id:
        if len(students_list) > 0:
            select_user = students_list[0]
            student_id = select_user.id
        else:
            flash('Студентов в этой группе пока не существует, обратитесь к администратору системы', 'warning')
            return redirect(url_for('main.home'))
    else:
        select_user = current_group.users.filter(User.id == student_id).first()
        if not select_user:
            flash('Выбранной группе такого студента не существует, обратитесь к администратору системы', 'warning')
            return redirect(url_for('main.home'))
    students = []
    for item in students_list:
        students.append({
            'id': item.id,
            'name': get_full_name(item)
        })
    attendance_subjects = Attendance.query.filter_by(group_id=group_id).group_by(Attendance.subject_id).all()
    subjects = []
    for i in attendance_subjects:
        subjects.append(i.subject)
    activity_by_user = Activity.query.filter(Activity.user_id == student_id).order_by(Activity.status).all()
    return render_template('rating.html',
                           title='Рейтинг УГАТУ',
                           group_id=group_id,
                           groups=groups,
                           students=students,
                           student_id=student_id,
                           subjects=subjects,
                           activity_by_user=activity_by_user,
                           active_tab='rating'
                           )


@deans_office.route('/activity/<string:activity_id>/group/<string:group_id>/student/<string:student_id>')
@login_required
def activity_accept(activity_id, group_id, student_id):
    activity = Activity.query.get_or_404(activity_id)
    activity.status = True
    db.session.commit()
    flash('Активность обновлена!', 'success')
    return redirect(url_for('deans_office.rating', group_id=group_id, student_id=student_id))


@deans_office.route('/activity/<string:activity_id>/group/<string:group_id>/student/<string:student_id>/decline',
                    methods=['GET', 'POST'])
@login_required
def activity_decline(activity_id, group_id, student_id):
    activity = Activity.query.get_or_404(activity_id)
    student = User.query.get_or_404(student_id)
    form = DeclineActivityForm()
    if form.validate_on_submit():
        activity.status = False
        activity.comment = form.comment.data
        db.session.commit()
        flash('Активность обновлена!', 'success')
        return redirect(url_for('deans_office.rating', group_id=group_id, student_id=student_id))
    return render_template('activity_decline.html',
                           title='Отклонить активную деаятельность',
                           group_id=group_id,
                           name_student=get_full_name(student),
                           student_id=student_id,
                           activity_id=activity_id,
                           form=form,
                           activity=activity
                           )


@deans_office.route('/admin')
@deans_office.route('/admin/<string:entity>')
@login_required
def admin(entity=None):
    groups = [{
        'name': 'Предметы',
        'url': '#',
        'id': SUBJECT
    }, {
        'name': 'Лабораторные работы',
        'url': '#',
        'id': LAB
    }, {
        'name': 'Рассписание',
        'url': '#',
        'id': ATTENDANCE
    }, {
        'name': 'Типы посешений',
        'url': '#',
        'id': ATTENDANCE_TYPE
    }, {
        'name': 'Оценки',
        'url': '#',
        'id': GRADE
    }, {
        'name': 'Типы оценок',
        'url': '#',
        'id': TYPE_GRADE
    }, {
        'name': 'Группы',
        'url': '#',
        'id': GROUP
    }, {
        'name': 'Роли',
        'url': '#',
        'id': ROLE
    }, {
        'name': 'Пользователи',
        'url': '#',
        'id': USER
    }, {
        'name': 'Типы активности',
        'url': '#',
        'id': ACTIVITY_TYPE
    }, {
        'name': 'Подтипы активности',
        'url': '#',
        'id': ACTIVITY_SUB_TYPE
    }, {
        'name': 'Рейтинг активности',
        'url': '#',
        'id': RATE_ACTIVITY
    }]
    if not entity:
        entity = groups[0]['id']
    if entity == SUBJECT:
        add_url, fields, entity_list_values = admin_subjects()
    elif entity == LAB:
        add_url, fields, entity_list_values = admin_lab()
    elif entity == ATTENDANCE:
        add_url, fields, entity_list_values = admin_attendance()
    return render_template('admin.html',
                           title='Администрирование',
                           entity=entity,
                           groups=groups,
                           fields=fields,
                           add_url=add_url,
                           entity_list_values=entity_list_values,
                           active_tab='admin')


def admin_subjects():
    add_url = '#'
    fields = ['Название', 'Количество часов']
    entity_list = Subject.query.order_by(Subject.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name, item.count_hours],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_lab():
    add_url = '#'
    fields = ['Название', 'Предмет', 'Дата', 'Дедлайн']
    entity_list = Lab.query.order_by(Lab.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name, item.subject.name, item.datetime.strftime('%d/%m/%Y'),
                      item.deadline.strftime('%d/%m/%Y')],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_attendance():
    add_url = '#'
    fields = ['Предмет', 'Группа', 'Тип', 'Дата']
    entity_list = Attendance.query.order_by(Attendance.date)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.subject.name, item.group.name, item.type.name, item.date.strftime('%d/%m/%Y')],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values
