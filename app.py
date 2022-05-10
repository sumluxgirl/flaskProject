from pointraing import app, db, bcrypt
from pointraing.models import Role, User, Group, Subject, Lab, AttendanceType, Attendance
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
        hashed_password=bcrypt.generate_password_hash('yakhina.ee123').decode('utf-8'),
        role=role_student,
        group=group424
    )
    student_norm = User(
        id=create_id(),
        surname='Шилов',
        name='Алексей',
        patronymic='Робертович',
        login='shilov.ar',
        hashed_password=bcrypt.generate_password_hash('shilov.ar123').decode('utf-8'),
        role=role_student,
        group=group321
    )
    student_bad = User(
        id=create_id(),
        surname='Ахкамова',
        name='Алина',
        patronymic='Радиковна',
        login='ahkamova.ar',
        hashed_password=bcrypt.generate_password_hash('ahkamova.ar123').decode('utf-8'),
        role=role_student,
        group=group424
    )
    student_very_bad = User(
        id=create_id(),
        surname='Павочкин',
        name='Ярослав',
        patronymic='Константичнович',
        login='pavochkin.yk',
        hashed_password=bcrypt.generate_password_hash('pavochkin.yk123').decode('utf-8'),
        role=role_student,
        group=group321
    )
    deans_office = User(
        id=create_id(),
        surname='Уразбахтина',
        name='Юлия',
        patronymic='Олеговна',
        login='urazbakhtina.yo',
        hashed_password=bcrypt.generate_password_hash('urazbakhtina.yo123').decode('utf-8'),
        role=role_deans_office
    )
    tutor = User(
        id=create_id(),
        surname='Жданов',
        name='Руслан',
        patronymic='Римович',
        login='zhdanov.rr',
        hashed_password=bcrypt.generate_password_hash('zhdanov.rr123').decode('utf-8'),
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
        tutor: tutor,
        deans_office: deans_office
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
    ),
    subject_telecommunication = Subject(
        id=create_id(),
        name='Системы сети и устройства телекоммуникации',
        count_hours=6
    )
    db.session.add_all(subject_comp_network, subject_line_transmission, subject_telecommunication)
    return {
        subject_comp_network,
        subject_line_transmission,
        subject_telecommunication
    }


def create_labs(subjects):
    lab_comp_network = Lab(
        id=create_id(),
        name='макет компьют. сети',
        subject=subjects.subject_comp_network,
        datetime=datetime.datetime(2021, 9, 20, 23, 59, 59),
        deadline=datetime.datetime(2021, 9, 27, 23, 59, 59)
    )
    lab_line_transmission = Lab(
        id=create_id(),
        name='макет многосвязной линии передач',
        subject=subjects.subject_1,
        datetime=datetime.datetime(2021, 9, 23, 23, 59, 59),
        deadline=datetime.datetime(2021, 9, 30, 23, 59, 59)
    )
    lab_telecommunication = Lab(
        id=create_id(),
        name='Создание системы сети и устройства телекоммуникации',
        subject=subjects.subject_1,
        datetime=datetime.datetime(2021, 9, 21, 23, 59, 59),
        deadline=datetime.datetime(2021, 9, 28, 23, 59, 59)
    )
    db.session.add_all(lab_comp_network, lab_line_transmission, lab_telecommunication)
    return {
        lab_comp_network,
        lab_line_transmission,
        lab_telecommunication
    }


def create_attendance():
    return None


def adding_data():
    db.drop_all()
    with app.app_context():
        db.create_all()
        users = create_users()
        subjects = create_subjects()
        labs = create_labs(subjects)
        db.session.commit()


adding_data()
