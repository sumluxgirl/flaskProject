from pointraing.models import Group, User, Attendance, ActivityType, Subject, Lab, AttendanceType, Grade, TypeGrade, \
    Role, ActivitySubType, RateActivity
from flask import url_for, flash, redirect, request, render_template
from pointraing.deans_office.forms import SubjectForm, LabForm, AttendanceForm, SimpleEntityForm
from pointraing import db
from pointraing.main.routes import create_id

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


def get_entities():
    return [{
        'name': 'Предметы',
        'id': SUBJECT
    }, {
        'name': 'Лабораторные работы',
        'id': LAB
    }, {
        'name': 'Рассписание',
        'id': ATTENDANCE
    }, {
        'name': 'Типы посешений',
        'id': ATTENDANCE_TYPE
    }, {
        'name': 'Оценки',
        'id': GRADE
    }, {
        'name': 'Типы оценок',
        'id': TYPE_GRADE
    }, {
        'name': 'Группы',
        'id': GROUP
    }, {
        'name': 'Роли',
        'id': ROLE
    }, {
        'name': 'Пользователи',
        'id': USER
    }, {
        'name': 'Типы активности',
        'id': ACTIVITY_TYPE
    }, {
        'name': 'Подтипы активности',
        'id': ACTIVITY_SUB_TYPE
    }, {
        'name': 'Рейтинг активности',
        'id': RATE_ACTIVITY
    }]


def get_entities_values():
    return {
        SUBJECT: admin_subject,
        LAB: admin_lab,
        ATTENDANCE: admin_attendance,
        ATTENDANCE_TYPE: admin_attendance_type,
        GRADE: admin_grade,
        TYPE_GRADE: admin_type_grade,
        GROUP: admin_group,
        ROLE: admin_role,
        USER: admin_user,
        ACTIVITY_TYPE: admin_activity_type,
        ACTIVITY_SUB_TYPE: admin_activity_sub_type,
        RATE_ACTIVITY: admin_rate_activity
    }


def admin_entities(entity_list, value, entity):
    entity_list_values = []
    for index, item in enumerate(entity_list):
        values = []
        for it_val in value:
            values.append(item.__dict__[it_val])
        entity_list_values.append({
            'idx': index + 1,
            'value': values,
            'action': {
                'edit': url_for('deans_office.entity_update', item_id=item.id, entity=entity),
                'delete': url_for('deans_office.entity_remove', item_id=item.id, entity=entity)
            }
        })
    return entity_list_values


def admin_simple_entity():
    fields = ['Название']
    values = ['name']
    return fields, values


def admin_subject():
    add_url = url_for('deans_office.entity_update', entity=SUBJECT)
    fields = ['Название', 'Количество часов']
    values = ['name', 'count_hours']
    entity_list = Subject.query.order_by(Subject.name)
    entity_list_values = admin_entities(entity_list, values, entity=SUBJECT)
    return add_url, fields, entity_list_values


def admin_lab():
    add_url = url_for('deans_office.entity_update', entity=LAB)
    fields = ['Название', 'Предмет', 'Дата', 'Дедлайн']
    entity_list = Lab.query.order_by(Lab.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name, item.subject.name, item.datetime.strftime('%d/%m/%Y'),
                      item.deadline.strftime('%d/%m/%Y')],
            'action': {
                'edit': url_for('deans_office.entity_update', item_id=item.id, entity=LAB),
                'delete': url_for('deans_office.entity_remove', item_id=item.id, entity=LAB)
            }
        })
    return add_url, fields, entity_list_values


def admin_attendance():
    add_url = url_for('deans_office.entity_update', entity=ATTENDANCE)
    fields = ['Предмет', 'Группа', 'Тип', 'Дата']
    entity_list = Attendance.query.order_by(Attendance.subject_id).order_by(Attendance.date)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.subject.name, item.group.name, item.type.name, item.date.strftime('%d/%m/%Y')],
            'action': {
                'edit': url_for('deans_office.entity_update', item_id=item.id, entity=ATTENDANCE),
                'delete': url_for('deans_office.entity_remove', item_id=item.id, entity=ATTENDANCE)
            }
        })
    return add_url, fields, entity_list_values


def admin_attendance_type():
    add_url = url_for('deans_office.entity_update', entity=ATTENDANCE_TYPE)
    fields, values = admin_simple_entity()
    entity_list = AttendanceType.query.order_by(AttendanceType.name)
    entity_list_values = admin_entities(entity_list, values, ATTENDANCE_TYPE)
    return add_url, fields, entity_list_values


def admin_grade():
    add_url = '#'
    fields = ['Предмет', 'Дата', 'Тип']
    entity_list = Grade.query.order_by(Grade.date)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.subject.name, item.date.strftime('%d/%m/%Y'), item.type.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_type_grade():
    add_url = '#'
    fields, values = admin_simple_entity()
    entity_list = TypeGrade.query.order_by(TypeGrade.name)
    entity_list_values = admin_entities(entity_list, values, TYPE_GRADE)
    return add_url, fields, entity_list_values


def admin_group():
    add_url = '#'
    fields, values = admin_simple_entity()
    entity_list = Group.query.order_by(Group.name)
    entity_list_values = admin_entities(entity_list, values, GROUP)
    return add_url, fields, entity_list_values


def admin_role():
    add_url = '#'
    fields, values = admin_simple_entity()
    entity_list = Role.query.order_by(Role.name)
    entity_list_values = admin_entities(entity_list, values, ROLE)
    return add_url, fields, entity_list_values


def admin_user():
    add_url = '#'
    fields = ['Имя', 'Фамилия', 'Отчество', 'Логин', 'Роль', 'Группа']
    entity_list = User.query.order_by(User.role_id)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name, item.surname, item.patronymic, item.login, item.role.name,
                      item.group.name if item.group else ''],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_activity_type():
    add_url = '#'
    fields, values = admin_simple_entity()
    entity_list = ActivityType.query.order_by(ActivityType.name)
    entity_list_values = admin_entities(entity_list, values, ACTIVITY_TYPE)
    return add_url, fields, entity_list_values


def admin_activity_sub_type():
    add_url = '#'
    fields, values = admin_simple_entity()
    entity_list = ActivitySubType.query.order_by(ActivitySubType.name)
    entity_list_values = admin_entities(entity_list, values, ACTIVITY_SUB_TYPE)
    return add_url, fields, entity_list_values


def admin_rate_activity():
    add_url = '#'
    fields = ['Тип', 'Подтип', 'Балл']
    entity_list = RateActivity.query.order_by(RateActivity.activity_type_id)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.type.name, item.sub_type.name if item.sub_type else '', item.value],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def subject_update(item_id, title, groups):
    subject = Subject.query.get_or_404(item_id) if item_id else None
    form = SubjectForm()
    if form.validate_on_submit():
        if subject:
            subject.name = form.name.data
            subject.count_hours = form.count_hours.data
        else:
            db.session.add(Subject(
                id=create_id(),
                name=form.name.data,
                count_hours=form.count_hours.data
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if subject else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=SUBJECT))
    elif request.method == 'GET' and subject:
        form.name.data = subject.name
        form.count_hours.data = subject.count_hours
    return render_template('subject_update.html',
                           title=title,
                           groups=groups,
                           entity=SUBJECT,
                           form=form
                           )


def entity_remove(row, entity):
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('deans_office.admin', entity=entity))


def subject_remove(item_id):
    return entity_remove(Subject.query.get_or_404(item_id), SUBJECT)


def lab_update(item_id, title, groups):
    lab = Lab.query.get_or_404(item_id) if item_id else None
    form = LabForm()
    form.subject.choices = [(g.id, g.name) for g in Subject.query.all()]
    if form.validate_on_submit():
        if lab:
            lab.name = form.name.data
            lab.subject_id = form.subject.data
            lab.datetime = form.datetime.data
            lab.deadline = form.deadline.data
        else:
            db.session.add(Lab(
                id=create_id(),
                name=form.name.data,
                subject_id=form.subject.data,
                datetime=form.datetime.data,
                deadline=form.deadline.data
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if item_id else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=LAB))
    elif request.method == 'GET' and item_id:
        form.name.data = lab.name
        form.subject.data = lab.subject_id
        form.datetime.data = lab.datetime
        form.deadline.data = lab.deadline
    return render_template('lab_update.html',
                           title=title,
                           groups=groups,
                           entity=LAB,
                           form=form
                           )


def lab_remove(item_id):
    return entity_remove(Lab.query.get_or_404(item_id), LAB)


def attendance_update(item_id, title, groups):
    attendance = Attendance.query.get_or_404(item_id) if item_id else None
    form = AttendanceForm()
    form.subject.choices = [(g.id, g.name) for g in Subject.query.all()]
    form.group.choices = [(g.id, g.name) for g in Group.query.all()]
    form.type.choices = [(g.id, g.name) for g in AttendanceType.query.all()]
    if form.validate_on_submit():
        if attendance:
            attendance.subject_id = form.subject.data
            attendance.group_id = form.group.data
            attendance.type_id = form.type.data
            attendance.date = form.date.data
        else:
            db.session.add(Attendance(
                id=create_id(),
                subject_id=form.subject.data,
                group_id=form.group.data,
                type_id=form.type.data,
                date=form.date.data,
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if item_id else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=ATTENDANCE))
    elif request.method == 'GET' and item_id:
        form.subject.data = attendance.subject_id
        form.group.data = attendance.group_id
        form.type.data = attendance.type_id
        form.date.data = attendance.date
    return render_template('attendance_admin_update.html',
                           title=title,
                           groups=groups,
                           entity=ATTENDANCE,
                           form=form
                           )


def attendance_remove(item_id):
    return entity_remove(Attendance.query.get_or_404(item_id), ATTENDANCE)


def simple_entity_update(item_id, title, groups, model, type):
    entity = model.query.get_or_404(item_id) if item_id else None
    form = SimpleEntityForm()
    if form.validate_on_submit():
        if entity:
            entity.name = form.name.data
        else:
            db.session.add(model(
                id=create_id(),
                name=form.name.data
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if item_id else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=type))
    elif request.method == 'GET' and item_id:
        form.name.data = entity.name
    return render_template('entity_update.html',
                           title=title,
                           groups=groups,
                           entity=type,
                           form=form
                           )


def attendance_type_update(item_id, title, groups):
    return simple_entity_update(item_id, title, groups, AttendanceType, ATTENDANCE_TYPE)


def attendance_type_remove(item_id):
    return entity_remove(AttendanceType.query.get_or_404(item_id), ATTENDANCE_TYPE)
