from pointraing.models import Group, User, Attendance, ActivityType, Subject, Lab, AttendanceType, Grade, TypeGrade, \
    Role, ActivitySubType, RateActivity

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


def admin_subject():
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
    entity_list = Attendance.query.order_by(Attendance.subject_id).order_by(Attendance.date)
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


def admin_attendance_type():
    add_url = '#'
    fields = ['Название']
    entity_list = AttendanceType.query.order_by(AttendanceType.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_grade():
    add_url = '#'
    fields = ['Предмет', 'Тип', 'Дата']
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
    fields = ['Название']
    entity_list = TypeGrade.query.order_by(TypeGrade.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_group():
    add_url = '#'
    fields = ['Название']
    entity_list = Group.query.order_by(Group.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_role():
    add_url = '#'
    fields = ['Название']
    entity_list = Role.query.order_by(Role.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
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
    fields = ['Название']
    entity_list = ActivityType.query.order_by(ActivityType.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
    return add_url, fields, entity_list_values


def admin_activity_sub_type():
    add_url = '#'
    fields = ['Название']
    entity_list = ActivitySubType.query.order_by(ActivitySubType.name)
    entity_list_values = []
    for index, item in enumerate(entity_list):
        entity_list_values.append({
            'idx': index + 1,
            'value': [item.name],
            'action': {
                'edit': '#',
                'delete': '#'
            }
        })
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
