from flask_login import current_user
import uuid

ROLE_STUDENT = 'b1cefe7269bd40bc97f74f0bcbcb5797'
ROLE_TUTOR = '45fbe5b876c740a98d11348ac6d43f92'
ROLE_DECANAT = 'f089ec17107041868d18827b3e5e1b53'


def is_student():
    return current_user.role.id == ROLE_STUDENT


def is_tutor():
    return current_user.role.id == ROLE_TUTOR


def is_deans_office():
    return current_user.role.id == ROLE_DECANAT


def get_full_name(item):
    return ' '.join([item.surname, item.name, item.patronymic])


def create_id():
    return uuid.uuid4().hex


def get_education_student_by_subject(student_id, subject_id):
    from pointraing.models import AttendanceGrade, Attendance, LabsGrade, Lab, GradeUsers, Grade, TypeGrade, User
    student = User.query.get_or_404(student_id)
    attendance_user = AttendanceGrade.query \
        .filter(AttendanceGrade.user_id == student.id).subquery()
    attendance = Attendance.query \
        .filter(Attendance.subject_id == subject_id) \
        .filter(Attendance.group_id == student.group_id) \
        .add_columns(attendance_user.c.id, attendance_user.c.active) \
        .outerjoin(attendance_user, Attendance.id == attendance_user.c.attendance_id) \
        .order_by(Attendance.date).all()
    attendance_count_user = AttendanceGrade.query \
        .join(AttendanceGrade.attendance) \
        .filter(Attendance.subject_id == subject_id) \
        .filter(AttendanceGrade.user_id == student.id) \
        .count()
    labs_user_subq = LabsGrade.query \
        .filter(LabsGrade.user_id == student.id).subquery()
    labs = Lab.query \
        .filter(Lab.subject_id == subject_id) \
        .add_columns(labs_user_subq.c.id, labs_user_subq.c.date) \
        .outerjoin(labs_user_subq, Lab.id == labs_user_subq.c.lab_id) \
        .all()
    labs_count_user = LabsGrade.query \
        .join(Lab, LabsGrade.lab) \
        .filter(Lab.subject_id == subject_id) \
        .filter(LabsGrade.user_id == student.id) \
        .count()
    grade = GradeUsers.query \
        .join(GradeUsers.grade) \
        .join(Grade.type) \
        .with_entities(GradeUsers.value, TypeGrade.name, Grade.date) \
        .filter(GradeUsers.user_id == student.id) \
        .filter(Grade.subject_id == subject_id) \
        .group_by(GradeUsers.id) \
        .all()

    return attendance_count_user, len(attendance), attendance, labs_count_user, len(labs), labs, grade
