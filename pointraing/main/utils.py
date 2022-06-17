from flask_login import current_user
import uuid

ROLE_STUDENT = 'b1cefe7269bd40bc97f74f0bcbcb5797'
ROLE_TUTOR = '45fbe5b876c740a98d11348ac6d43f92'
ROLE_DECANAT = 'f089ec17107041868d18827b3e5e1b53'

EXAM_ID = 'ee4213bae38f44989f9716b6fccd440e'
OFFSET_ID = 'a7f586cca2bf41f2846de0bb67bc2109'


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
    from pointraing import db
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

    group_id = student.group_id
    grade_xpr, offset_xpr, attendance_grade_sq, lab_grade_sq = get_analyze_grade(subject_id, group_id)
    auto_grade = db.session.query(grade_xpr.label('exam'), offset_xpr.label('offset')) \
        .select_from(User) \
        .filter(User.id == student_id) \
        .outerjoin(attendance_grade_sq, attendance_grade_sq.c.user_id == User.id) \
        .outerjoin(lab_grade_sq, lab_grade_sq.c.user_id == User.id) \
        .group_by(User.id) \
        .first()

    return attendance_count_user, len(attendance), attendance, labs_count_user, len(labs), labs, grade, auto_grade


def get_analyze_grade(subject_id, group_id):
    from sqlalchemy.sql import func, case, and_
    from pointraing.models import Attendance, AttendanceGrade, LabsGrade, Lab
    attendance_sq = Attendance.query \
        .with_entities(Attendance.id) \
        .filter(Attendance.subject_id == subject_id) \
        .filter(Attendance.group_id == group_id)
    attendance_grade_sq = AttendanceGrade.query \
        .with_entities(AttendanceGrade.id, AttendanceGrade.user_id, AttendanceGrade.active) \
        .filter(AttendanceGrade.attendance_id.in_(attendance_sq)).subquery()
    attendance_user_xpr = case([(attendance_grade_sq.c.id.is_not(None), 1)], else_=0)
    attendance_active_user_xpr = case([(attendance_grade_sq.c.active.is_not(None), attendance_grade_sq.c.active)],
                                      else_=0)
    labs_sq_xpr = case([(LabsGrade.date < Lab.deadline, 1)], else_=0)
    lab_grade_sq = LabsGrade.query \
        .with_entities(LabsGrade.user_id,
                       func.sum(labs_sq_xpr).label('in_time_count'),
                       func.count(LabsGrade.id).label('count')
                       ) \
        .join(Lab) \
        .filter(Lab.subject_id == subject_id) \
        .group_by(LabsGrade.user_id).subquery()
    max_attendance_count = attendance_sq.count()
    max_lab_count = Lab.query.filter(Lab.subject_id == subject_id).count()
    attendance_count = func.sum(attendance_user_xpr).label('attendance_count')
    attendance_active_count = func.sum(attendance_active_user_xpr).label('attendance_active_count')
    lab_in_time_count = lab_grade_sq.c.in_time_count.label('lab_in_time_count')
    lab_count = lab_grade_sq.c.count.label('lab_count')
    attendance_count_user = attendance_count * 100 / max_attendance_count
    attendance_active_count_user = attendance_active_count * 100 / max_attendance_count
    lab_in_time_user_count = lab_in_time_count * 100 / max_lab_count
    excellent_xpr = case([(and_(attendance_count_user >= 75,
                                attendance_active_count_user >= 50,
                                lab_in_time_user_count == 100), 5)], else_=0)
    good_xpr = case([(and_(attendance_count_user >= 60,
                           attendance_active_count_user >= 30,
                           lab_in_time_user_count >= 50), 4)], else_=0)
    adequately_xpr = case([(and_(attendance_count_user >= 50,
                                 attendance_active_count_user >= 10,
                                 lab_count / max_lab_count == 1), 3)], else_=0)
    offset_xpr = case([(and_(attendance_count_user >= 60,
                             attendance_active_count_user >= 40,
                             lab_in_time_user_count >= 50), 1)], else_=0)
    grade_xpr = func.max(excellent_xpr, good_xpr, adequately_xpr)

    return grade_xpr, offset_xpr, attendance_grade_sq, lab_grade_sq
