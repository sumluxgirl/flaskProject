from pointraing.models import Group, User, Attendance, ActivityType, Subject, Lab, AttendanceType, Grade, TypeGrade, \
    Role, ActivitySubType, RateActivity
from flask import url_for, flash, redirect, request, render_template
from pointraing.deans_office.forms import SubjectForm, LabForm, AttendanceForm, SimpleEntityForm, GradeForm, UserForm, \
    RateActivityForm
from pointraing import db, bcrypt
from pointraing.main.routes import create_id, ROLE_STUDENT

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


def get_url_action(item_id, entity):
    return {
        'edit': url_for('deans_office.entity_update', item_id=item_id, entity=entity),
        'delete': url_for('deans_office.entity_remove', item_id=item_id, entity=entity)
    }


def get_add_url(entity):
    return url_for('deans_office.entity_update', entity=entity)


def admin_entities(entity_list, value, entity):
    entity_list_values = []
    for index, item in enumerate(entity_list):
        values = []
        for it_val in value:
            values.append(item.__dict__[it_val])
        entity_list_values.append({
            'idx': index + 1,
            'value': values,
            'action': get_url_action(item_id=item.id, entity=entity)
        })
    return entity_list_values


def admin_simple_entity(entity, entity_list):
    add_url = get_add_url(entity)
    fields = ['Название']
    values = ['name']
    entity_list_values = admin_entities(entity_list, values, entity)
    return add_url, fields, entity_list_values


def admin_subject():
    entity = SUBJECT
    add_url = get_add_url(entity)
    fields = ['Название', 'Количество часов']
    values = ['name', 'count_hours']
    entity_list = Subject.query.order_by(Subject.name)
    entity_list_values = admin_entities(entity_list, values, entity)
    return add_url, fields, entity_list_values


def admin_lab():
    entity = LAB
    add_url = get_add_url(entity)
    fields = ['Название', 'Предмет', 'Дата', 'Дедлайн']
    entity_list = Lab.query.order_by(Lab.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name, item.subject.name, item.datetime.strftime('%d/%m/%Y'),
                      item.deadline.strftime('%d/%m/%Y')],
            'action': get_url_action(item.id, entity)
        })
    return add_url, fields, entity_list_values


def admin_attendance():
    entity = ATTENDANCE
    add_url = get_add_url(entity)
    fields = ['Предмет', 'Группа', 'Тип', 'Дата']
    entity_list = Attendance.query.order_by(Attendance.subject_id).order_by(Attendance.date)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.subject.name, item.group.name, item.type.name, item.date.strftime('%d/%m/%Y')],
            'action': get_url_action(item.id, entity)
        })
    return add_url, fields, entity_list_values


def admin_attendance_type():
    entity = ATTENDANCE_TYPE
    entity_list = AttendanceType.query.order_by(AttendanceType.name)
    return admin_simple_entity(entity, entity_list)


def admin_grade():
    entity = GRADE
    add_url = get_add_url(entity)
    fields = ['Предмет', 'Дата', 'Тип']
    entity_list = Grade.query.order_by(Grade.date)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.subject.name, item.date.strftime('%d/%m/%Y'), item.type.name],
            'action': get_url_action(item.id, entity)
        })
    return add_url, fields, entity_list_values


def admin_type_grade():
    entity = TYPE_GRADE
    entity_list = TypeGrade.query.order_by(TypeGrade.name)
    return admin_simple_entity(entity, entity_list)


def admin_group():
    entity = GROUP
    entity_list = Group.query.order_by(Group.name)
    return admin_simple_entity(entity, entity_list)


def admin_role():
    entity = ROLE
    entity_list = Role.query.order_by(Role.name)
    return admin_simple_entity(entity, entity_list)


def admin_user():
    entity = USER
    add_url = get_add_url(entity)
    fields = ['Имя', 'Фамилия', 'Отчество', 'Логин', 'Роль', 'Группа']
    entity_list = User.query.order_by(User.role_id)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name, item.surname, item.patronymic, item.login, item.role.name,
                      item.group.name if item.group else ''],
            'action': get_url_action(item.id, entity)
        })
    return add_url, fields, entity_list_values


def admin_activity_type():
    entity = ACTIVITY_TYPE
    entity_list = ActivityType.query.order_by(ActivityType.name)
    return admin_simple_entity(entity, entity_list)


def admin_activity_sub_type():
    entity = ACTIVITY_SUB_TYPE
    entity_list = ActivitySubType.query.order_by(ActivitySubType.name)
    return admin_simple_entity(entity, entity_list)


def admin_rate_activity():
    entity = RATE_ACTIVITY
    add_url = get_add_url(entity)
    fields = ['Тип', 'Подтип', 'Балл']
    entity_list = RateActivity.query.order_by(RateActivity.activity_type_id)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.type.name, item.sub_type.name if item.sub_type else '', item.value],
            'action': get_url_action(item.id, entity)
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


def grade_update(item_id, title, groups):
    grade = Grade.query.get_or_404(item_id) if item_id else None
    form = GradeForm()
    form.subject.choices = [(g.id, g.name) for g in Subject.query.all()]
    form.type.choices = [(g.id, g.name) for g in TypeGrade.query.all()]
    if form.validate_on_submit():
        if grade:
            grade.subject_id = form.subject.data
            grade.type_id = form.type.data
            grade.date = form.date.data
        else:
            db.session.add(Grade(
                id=create_id(),
                subject_id=form.subject.data,
                type_id=form.type.data,
                date=form.date.data,
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if item_id else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=GRADE))
    elif request.method == 'GET' and item_id:
        form.subject.data = grade.subject_id
        form.type.data = grade.type_id
        form.date.data = grade.date
    return render_template('grade_update.html',
                           title=title,
                           groups=groups,
                           entity=GRADE,
                           form=form
                           )


def grade_remove(item_id):
    return entity_remove(Grade.query.get_or_404(item_id), GRADE)


def type_grade_update(item_id, title, groups):
    return simple_entity_update(item_id, title, groups, TypeGrade, TYPE_GRADE)


def type_grade_remove(item_id):
    return entity_remove(TypeGrade.query.get_or_404(item_id), TYPE_GRADE)


def group_update(item_id, title, groups):
    return simple_entity_update(item_id, title, groups, Group, GROUP)


def group_remove(item_id):
    return entity_remove(Group.query.get_or_404(item_id), GROUP)


def role_update(item_id, title, groups):
    return simple_entity_update(item_id, title, groups, Role, ROLE)


def role_remove(item_id):
    return entity_remove(Role.query.get_or_404(item_id), ROLE)


def activity_type_update(item_id, title, groups):
    return simple_entity_update(item_id, title, groups, ActivityType, ACTIVITY_TYPE)


def activity_type_remove(item_id):
    return entity_remove(ActivityType.query.get_or_404(item_id), ACTIVITY_TYPE)


def activity_sub_type_update(item_id, title, groups):
    return simple_entity_update(item_id, title, groups, ActivitySubType, ACTIVITY_SUB_TYPE)


def activity_sub_type_remove(item_id):
    return entity_remove(ActivitySubType.query.get_or_404(item_id), ACTIVITY_SUB_TYPE)


def user_update(item_id, title, groups):
    user = User.query.get_or_404(item_id) if item_id else None
    form = UserForm()
    form.role.choices = [(g.id, g.name) for g in Role.query.all()]
    form.group.choices = [(g.id, g.name) for g in Group.query.all()]
    if not item_id:
        from wtforms.validators import DataRequired
        form.password.validators = [DataRequired()]
    if form.validate_on_submit():
        if user:
            if form.password.data:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
            user.surname = form.surname.data
            user.name = form.name.data
            user.patronymic = form.patronymic.data
            user.login = form.login.data
            user.role_id = form.role.data
            user.group_id = form.group.data if form.role.data == ROLE_STUDENT else None
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.add(User(
                id=create_id(),
                surname=form.surname.data,
                name=form.name.data,
                patronymic=form.patronymic.data,
                login=form.login.data,
                password=hashed_password,
                role_id=form.role.data,
                group_id=form.group.data if form.role.data == ROLE_STUDENT else None
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if item_id else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=USER))
    elif request.method == 'GET' and item_id:
        form.surname.data = user.surname
        form.name.data = user.name
        form.patronymic.data = user.patronymic
        form.login.data = user.login
        form.role.data = user.role_id
        form.group.data = user.group_id if form.role.data == ROLE_STUDENT else None
    return render_template('user_update.html',
                           title=title,
                           groups=groups,
                           entity=USER,
                           form=form
                           )


def user_remove(item_id):
    return entity_remove(User.query.get_or_404(item_id), USER)


def rate_activity_update(item_id, title, groups):
    rate = RateActivity.query.get_or_404(item_id) if item_id else None
    form = RateActivityForm()
    form.type.choices = [(g.id, g.name) for g in ActivityType.query.all()]
    form.sub_type.choices = [(g.id, g.name) for g in ActivitySubType.query.all()]
    if form.validate_on_submit():
        if rate:
            rate.activity_type_id = form.type.data
            rate.activity_sub_type_id = form.sub_type.data
            rate.value = form.value.data
        else:
            db.session.add(RateActivity(
                id=create_id(),
                activity_type_id=form.type.data,
                activity_sub_type_id=form.sub_type.data,
                value=form.value.data
            ))
        db.session.commit()
        flash('Запись изменена!', 'success') if item_id else flash('Запись добавлена!', 'success')
        return redirect(url_for('deans_office.admin', entity=RATE_ACTIVITY))
    elif request.method == 'GET' and item_id:
        form.type.data = rate.activity_type_id
        form.sub_type.data = rate.activity_sub_type_id
        form.value.data = rate.value
    return render_template('rate_activity_update.html',
                           title=title,
                           groups=groups,
                           entity=RATE_ACTIVITY,
                           form=form
                           )


def rate_activity_remove(item_id):
    return entity_remove(RateActivity.query.get_or_404(item_id), RATE_ACTIVITY)
