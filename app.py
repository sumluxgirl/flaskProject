from pointraing import app, db, bcrypt
from pointraing.models import Role, User, Group, Subject, Lab, AttendanceType, Attendance, ActivityType, \
    ActivitySubType, RateActivity, AttendanceGrade, LabsGrade
import datetime
import uuid

if __name__ == '__main__':
    app.run(debug=True)


def create_id():
    return uuid.uuid4().hex


def create_users():
    role_student = Role(id=create_id(), name='Студент')
    role_tutor = Role(id=create_id(), name='Преподавательь')
    role_deans_office = Role(id=create_id(), name='Деканат')
    group424 = Group(id=create_id(), name='ИКТ-424')
    group321 = Group(id=create_id(), name='ИКТ-321')
    student_best = User(
        id=create_id(),
        surname='Яхина',
        name='Элина',
        patronymic='Эльмаровна',
        login='yakhina.ee',
        password=bcrypt.generate_password_hash('yakhina.ee123').decode('utf-8'),
        role=role_student,
        group=group424
    )
    student_norm = User(
        id=create_id(),
        surname='Шилов',
        name='Алексей',
        patronymic='Робертович',
        login='shilov.ar',
        password=bcrypt.generate_password_hash('shilov.ar123').decode('utf-8'),
        role=role_student,
        group=group321
    )
    student_bad = User(
        id=create_id(),
        surname='Ахкамова',
        name='Алина',
        patronymic='Радиковна',
        login='ahkamova.ar',
        password=bcrypt.generate_password_hash('ahkamova.ar123').decode('utf-8'),
        role=role_student,
        group=group424
    )
    student_very_bad = User(
        id=create_id(),
        surname='Павочкин',
        name='Ярослав',
        patronymic='Константичнович',
        login='pavochkin.yk',
        password=bcrypt.generate_password_hash('pavochkin.yk123').decode('utf-8'),
        role=role_student,
        group=group321
    )
    deans_office = User(
        id=create_id(),
        surname='Уразбахтина',
        name='Юлия',
        patronymic='Олеговна',
        login='urazbakhtina.yo',
        password=bcrypt.generate_password_hash('urazbakhtina.yo123').decode('utf-8'),
        role=role_deans_office
    )
    tutor = User(
        id=create_id(),
        surname='Жданов',
        name='Руслан',
        patronymic='Римович',
        login='zhdanov.rr',
        password=bcrypt.generate_password_hash('zhdanov.rr123').decode('utf-8'),
        role=role_tutor
    )
    db.session.add_all([
        role_student, role_tutor, role_deans_office, group424, group321, student_best, student_norm, student_bad,
        student_very_bad, tutor, deans_office
    ])
    return {
        'students': {
            'student_best': student_best,
            'student_norm': student_norm,
            'student_bad': student_bad,
            'student_very_bad': student_very_bad
        },
        'tutor': tutor,
        'deans_office': deans_office,
        'groups': {
            'group424': group424,
            'group321': group321
        }
    }


def create_subjects():
    subject_comp_network = Subject(
        id=create_id(),
        name='Компьютерные сети',
        count_hours=6
    )
    subject_line_transmission = Subject(
        id=create_id(),
        name='Многосвязные линии передач',
        count_hours=6
    )
    subject_telecommunication = Subject(
        id=create_id(),
        name='Системы сети и устройства телекоммуникации',
        count_hours=6
    )
    db.session.add_all([subject_comp_network, subject_line_transmission, subject_telecommunication])
    return {
        'subject_comp_network': subject_comp_network,
        'subject_line_transmission': subject_line_transmission,
        'subject_telecommunication': subject_telecommunication
    }


def create_labs(subjects):
    lab_comp_network = Lab(
        id=create_id(),
        name='макет компьют. сети',
        subject=subjects['subject_comp_network'],
        datetime=datetime.datetime(2021, 9, 20, 0, 0, 0),
        deadline=datetime.datetime(2021, 9, 27, 23, 59, 59)
    )
    lab_line_transmission = Lab(
        id=create_id(),
        name='макет многосвязной линии передач',
        subject=subjects['subject_line_transmission'],
        datetime=datetime.datetime(2021, 9, 23, 0, 0, 0),
        deadline=datetime.datetime(2021, 9, 30, 23, 59, 59)
    )
    lab_telecommunication = Lab(
        id=create_id(),
        name='Создание системы сети и устройства телекоммуникации',
        subject=subjects['subject_telecommunication'],
        datetime=datetime.datetime(2021, 9, 21, 0, 0, 0),
        deadline=datetime.datetime(2021, 9, 28, 23, 59, 59)
    )
    db.session.add_all([lab_comp_network, lab_line_transmission, lab_telecommunication])
    return {
        'lab_comp_network': lab_comp_network,
        'lab_line_transmission': lab_line_transmission,
        'lab_telecommunication': lab_telecommunication
    }


def create_attendance(subjects, groups):
    lecture = AttendanceType(id=create_id(), name='Лекция')
    practice = AttendanceType(id=create_id(), name='Практика')
    attendance_424 = {
        'comp_network': [
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group424'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 3, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group424'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 10, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group424'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 14, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group424'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 16, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group424'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 23, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group424'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 30, 0, 0, 0),
                       )
        ],
        'line_transmission': [
            Attendance(id=create_id(),
                       subject=subjects['subject_line_transmission'],
                       group=groups['group424'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 1, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_line_transmission'],
                       group=groups['group424'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 8, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_line_transmission'],
                       group=groups['group424'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 15, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_line_transmission'],
                       group=groups['group424'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 13, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_line_transmission'],
                       group=groups['group424'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 20, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_line_transmission'],
                       group=groups['group424'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 27, 0, 0, 0),
                       )
        ]
    }
    attendance_321 = {
        'comp_network': [
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group321'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 2, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group321'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 19, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group321'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 16, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group321'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 14, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group321'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 21, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_comp_network'],
                       group=groups['group321'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 29, 0, 0, 0),
                       )
        ],
        'telecommunication': [
            Attendance(id=create_id(),
                       subject=subjects['subject_telecommunication'],
                       group=groups['group321'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 4, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_telecommunication'],
                       group=groups['group321'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 11, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_telecommunication'],
                       group=groups['group321'],
                       type=lecture,
                       date=datetime.datetime(2021, 9, 18, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_telecommunication'],
                       group=groups['group321'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 15, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_telecommunication'],
                       group=groups['group321'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 22, 0, 0, 0),
                       ),
            Attendance(id=create_id(),
                       subject=subjects['subject_telecommunication'],
                       group=groups['group321'],
                       type=practice,
                       date=datetime.datetime(2021, 9, 29, 0, 0, 0),
                       )
        ]
    }
    db.session.add_all([lecture, practice])
    db.session.add_all(attendance_424['comp_network'])
    db.session.add_all(attendance_424['line_transmission'])
    db.session.add_all(attendance_321['comp_network'])
    db.session.add_all(attendance_321['telecommunication'])
    return {
        '424': attendance_424,
        '321': attendance_321
    }


def create_activity():
    activity_type_culture = ActivityType(id=create_id(), name="Культурная деятельность")
    activity_type_science = ActivityType(id=create_id(), name="Научная деятельность")
    activity_type_society = ActivityType(id=create_id(), name="Общественная деятельность")
    activity_type_sport = ActivityType(id=create_id(), name="Спортивная деятельность")
    activity_sub_type_local = ActivitySubType(id=create_id(), name="Республиканский")
    activity_sub_type_country = ActivitySubType(id=create_id(), name="Всероссийский")
    activity_sub_type_world = ActivitySubType(id=create_id(), name="Международный")

    rate_culture_local = RateActivity(id=create_id(),
                                      type=activity_type_culture,
                                      sub_type=activity_sub_type_local,
                                      value=1
                                      )
    rate_culture_country = RateActivity(id=create_id(),
                                        type=activity_type_culture,
                                        sub_type=activity_sub_type_country,
                                        value=2
                                        )
    rate_culture_world = RateActivity(id=create_id(),
                                      type=activity_type_culture,
                                      sub_type=activity_sub_type_world,
                                      value=2
                                      )
    rate_science = RateActivity(id=create_id(),
                                type=activity_type_science,
                                value=2
                                )
    rate_society = RateActivity(id=create_id(),
                                type=activity_type_society,
                                value=1
                                )
    rate_sport_local = RateActivity(id=create_id(),
                                    type=activity_type_sport,
                                    sub_type=activity_sub_type_local,
                                    value=1
                                    )
    rate_sport_country = RateActivity(id=create_id(),
                                      type=activity_type_sport,
                                      sub_type=activity_sub_type_country,
                                      value=2
                                      )
    rate_sport_world = RateActivity(id=create_id(),
                                    type=activity_type_sport,
                                    sub_type=activity_sub_type_world,
                                    value=2
                                    )

    db.session.add_all(
        [rate_culture_local, rate_culture_country, rate_culture_world, rate_science, rate_society, rate_sport_local,
         rate_sport_country, rate_sport_world])
    return {
        rate_culture_local, rate_culture_country, rate_culture_world, rate_science, rate_society, rate_sport_local,
        rate_sport_country, rate_sport_world
    }


def create_rate_users(users, attendance, labs):
    students = users['students']
    tutor = users['tutor']

    def add_attendance_424(attendance_item):
        db.session.add(
            AttendanceGrade(id=create_id(),
                            user_id=tutor.id,
                            student=students['student_best'],
                            attendance=attendance_item
                            )
        )
        if i.type.name == 'Практика':
            db.session.add(
                AttendanceGrade(id=create_id(),
                                user_id=tutor.id,
                                student=students['student_bad'],
                                attendance=attendance_item
                                )
            )

    for i in attendance['424']['comp_network']:
        add_attendance_424(i)

    for i in attendance['424']['line_transmission']:
        add_attendance_424(i)

    num = 0
    for i in attendance['321']['comp_network']:
        num = num + 1
        if num == 3 or i.type.name == 'Практика':
            db.session.add(
                AttendanceGrade(id=create_id(),
                                user_id=tutor.id,
                                student=students['student_norm'],
                                attendance=i
                                )
            )

    num = 0
    for i in attendance['321']['telecommunication']:
        num = num + 1
        if i.type.name == 'Практика':
            if num == 1:
                continue
            elif num == 2:
                db.session.add_all([
                    AttendanceGrade(id=create_id(),
                                    user_id=tutor.id,
                                    student=students['student_very_bad'],
                                    attendance=i
                                    ),
                    db.session.add(
                        AttendanceGrade(id=create_id(),
                                        user_id=tutor.id,
                                        student=students['student_norm'],
                                        attendance=i
                                        )
                    )
                ])
            else:
                db.session.add(
                    AttendanceGrade(id=create_id(),
                                    user_id=tutor.id,
                                    student=students['student_norm'],
                                    attendance=i
                                    )
                )
        else:
            db.session.add(
                AttendanceGrade(id=create_id(),
                                user_id=tutor.id,
                                student=students['student_norm'],
                                attendance=i
                                )
            )

    db.session.add_all([
        LabsGrade(id=create_id(),
                  lab=labs['lab_comp_network'],
                  user_id=tutor.id,
                  student=students['student_best'],
                  date=datetime.datetime(2021, 9, 25, 0, 0, 0)
                  ),
        LabsGrade(id=create_id(),
                  lab=labs['lab_line_transmission'],
                  user_id=tutor.id,
                  student=students['student_best'],
                  date=datetime.datetime(2021, 9, 28, 0, 0, 0)
                  ),
        LabsGrade(id=create_id(),
                  lab=labs['lab_comp_network'],
                  user_id=tutor.id,
                  student=students['student_bad'],
                  date=datetime.datetime(2021, 9, 27, 0, 0, 0)
                  ),
        LabsGrade(id=create_id(),
                  lab=labs['lab_line_transmission'],
                  user_id=tutor.id,
                  student=students['student_bad'],
                  date=datetime.datetime(2021, 9, 30, 0, 0, 0)
                  ),
        LabsGrade(id=create_id(),
                  lab=labs['lab_comp_network'],
                  user_id=tutor.id,
                  student=students['student_norm'],
                  date=datetime.datetime(2021, 9, 27, 0, 0, 0)
                  ),
        LabsGrade(id=create_id(),
                  lab=labs['lab_telecommunication'],
                  user_id=tutor.id,
                  student=students['student_norm'],
                  date=datetime.datetime(2021, 10, 4, 0, 0, 0)
                  ),
        LabsGrade(id=create_id(),
                  lab=labs['lab_comp_network'],
                  user_id=tutor.id,
                  student=students['student_very_bad'],
                  date=datetime.datetime(2021, 9, 30, 0, 0, 0)
                  )
    ])

def adding_data():
    db.drop_all()
    with app.app_context():
        db.create_all()
        users = create_users()
        subjects = create_subjects()
        labs = create_labs(subjects)
        attendance = create_attendance(subjects, users['groups'])
        activity = create_activity()
        create_rate_users(users, attendance, labs)
        db.session.commit()


adding_data()
