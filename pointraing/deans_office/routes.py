from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from pointraing.models import Group, User, Attendance, Activity, AttendanceGrade, Lab, LabsGrade, Grade, GradeUsers, \
    TypeGrade, RateActivity, Subject
from pointraing.main.routes import get_full_name, get_education_student_by_subject
from pointraing import db
from pointraing.deans_office.forms import DeclineActivityForm
from sqlalchemy.sql import func, case, desc

deans_office = Blueprint('deans_office', __name__, template_folder='templates')


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
    students_list = get_students_list_with_rating(group_id)
    if not student_id:
        if len(students_list) > 0:
            select_user = students_list[0].User
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
        current_student_id = item.User.id
        students.append({
            'id': current_student_id,
            'name': get_full_name(item.User),
            'count': item.count
        })
    subjects, subjects_count, subjects_max_count = get_user_subjects_rating(group_id, student_id)
    activity_by_user, activity_by_user_count = get_user_activity_rating(student_id)
    return render_template('rating.html',
                           title='Рейтинг УГАТУ',
                           group_id=group_id,
                           groups=groups,
                           students=students,
                           student_id=student_id,
                           subjects=subjects,
                           subjects_max_count=subjects_max_count,
                           subjects_count=subjects_count,
                           activity_by_user=activity_by_user,
                           activity_by_user_count=activity_by_user_count.sum_activity if activity_by_user_count else 0,
                           active_tab='rating'
                           )


def get_attendance_rating_by_user(student_id, subject_id, subject, attendance_sq):
    attendance_count = 0
    attendance_user = AttendanceGrade.query \
        .with_entities(AttendanceGrade.active) \
        .filter(AttendanceGrade.user_id == student_id) \
        .filter(AttendanceGrade.attendance_id
                .in_(attendance_sq
                     .with_entities(Attendance.id)
                     .filter(Attendance.subject_id == subject_id))
                ) \
        .all()
    for attendance_item in attendance_user:
        attendance_count = attendance_count + 1
        if attendance_item.active > 0:
            attendance_count = attendance_count + attendance_item.active
    attendance_max_count = subject.count_hours * 2
    return attendance_count, attendance_max_count


def get_labs_rating_by_user(student_id, subject_id):
    lab_count = 0
    lab_sq = Lab.query.with_entities(Lab.id).filter(Lab.subject_id == subject_id)
    lab_user = LabsGrade.query \
        .filter(LabsGrade.user_id == student_id) \
        .filter(LabsGrade.lab_id.in_(lab_sq)).all()
    for item_lab_user in lab_user:
        if (item_lab_user.date - item_lab_user.lab.deadline).total_seconds() < 0:
            lab_count = lab_count + 2
        else:
            lab_count = lab_count + 1
    lab_max_count = lab_sq.count() * 2
    return lab_count, lab_max_count


def get_grades_rating_by_user(student_id, subject_id):
    grade_count = 0
    grade_sq = Grade.query.with_entities(Grade.id).filter(Grade.subject_id == subject_id)
    grade_type_sq = grade_sq.join(Grade.type).group_by(Grade.id)
    grade_user = GradeUsers.query \
        .with_entities(GradeUsers.value) \
        .filter(GradeUsers.user_id == student_id) \
        .filter(GradeUsers.grade_id.in_(grade_sq)).all()
    for item_grade_user in grade_user:
        grade_count = grade_count + item_grade_user.value

    grade_max_count = grade_type_sq.filter(TypeGrade.name == 'Экзамен').count() * 5 + grade_type_sq.filter(
        TypeGrade.name == 'Зачет').count()
    return grade_count, grade_max_count


def get_user_rating_by_subject(subject, student_id, attendance_sq):
    subject_id = subject.id
    attendance_count, attendance_max_count = get_attendance_rating_by_user(student_id, subject_id, subject,
                                                                           attendance_sq)
    lab_count, lab_max_count = get_labs_rating_by_user(student_id, subject_id)
    grade_count, grade_max_count = get_grades_rating_by_user(student_id, subject_id)
    count_subj = attendance_count + lab_count + grade_count
    max_count = attendance_max_count + lab_max_count + grade_max_count
    subject_rating = {
        'id': subject_id,
        'name': subject.name,
        'attendance_max_count': attendance_max_count,
        'attendance_count': attendance_count,
        'lab_max_count': lab_max_count,
        'lab_count': lab_count,
        'grade_max_count': grade_max_count,
        'grade_count': grade_count,
        'count_subj': count_subj,
        'max_count': max_count
    }
    return count_subj, max_count, subject_rating


def get_user_subjects_rating(group_id, student_id):
    attendance_sq = Attendance.query.filter_by(group_id=group_id)
    attendance_subjects = attendance_sq.group_by(Attendance.subject_id).all()
    subjects = []
    subjects_count = 0
    subjects_max_count = 0
    for i in attendance_subjects:
        subject = i.subject
        count_subj, max_count, subject_rating = get_user_rating_by_subject(subject, student_id, attendance_sq)
        subjects.append(subject_rating)
        subjects_max_count = subjects_max_count + max_count
        subjects_count = subjects_count + count_subj
    return subjects, subjects_count, subjects_max_count


def get_user_activity_rating(student_id):
    activity_by_user = Activity.query.filter(Activity.user_id == student_id).order_by(Activity.status).all()
    activity_by_user_count = Activity.query \
        .join(Activity.rate) \
        .with_entities(func.sum(RateActivity.value).label('sum_activity')) \
        .filter(Activity.user_id == student_id).filter(Activity.status == True) \
        .group_by(Activity.id).first()
    return activity_by_user, activity_by_user_count


def get_students_list_with_rating(group_id):
    grade_sq = GradeUsers.query \
        .with_entities(GradeUsers.user_id, func.sum(GradeUsers.value).label('count')) \
        .group_by(GradeUsers.user_id).subquery()
    grade_sq_xpr = case([(grade_sq.c.count != None, grade_sq.c.count)],
                        else_=0)
    activity_sq = Activity.query \
        .join(RateActivity) \
        .with_entities(Activity.user_id,
                       func.sum(RateActivity.value).label('count')
                       ) \
        .filter(Activity.status == True) \
        .group_by(Activity.user_id).subquery()
    activity_xpr = case([(activity_sq.c.count != None, activity_sq.c.count)],
                        else_=0)
    attendance_sq_xpr = case([(AttendanceGrade.active != 0, 2)], else_=1)
    attendance_sq = AttendanceGrade.query \
        .with_entities(AttendanceGrade.user_id, func.sum(attendance_sq_xpr).label('count')) \
        .group_by(AttendanceGrade.user_id).subquery()
    attendance_xpr = case([(attendance_sq.c.count != None, attendance_sq.c.count)],
                          else_=0)
    labs_sq_xpr = case([(LabsGrade.date < Lab.deadline, 2)], else_=1)
    labs_sq = LabsGrade.query \
        .join(Lab) \
        .with_entities(LabsGrade.user_id,
                       func.sum(labs_sq_xpr).label('count')) \
        .group_by(LabsGrade.user_id).subquery()
    labs_xpr = case([(labs_sq.c.count != None, labs_sq.c.count)],
                    else_=0)
    students_list = User.query \
        .add_columns(func.sum(grade_sq_xpr + activity_xpr + attendance_xpr + labs_xpr).label('count')) \
        .outerjoin(grade_sq, grade_sq.c.user_id == User.id) \
        .outerjoin(activity_sq, activity_sq.c.user_id == User.id) \
        .outerjoin(attendance_sq, attendance_sq.c.user_id == User.id) \
        .outerjoin(labs_sq, labs_sq.c.user_id == User.id) \
        .filter(User.group_id == group_id) \
        .group_by(User.id) \
        .order_by(desc('count')).all()
    return students_list


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


@deans_office.route('/rating/student/<string:student_id>/subject/<string:subject_id>')
@login_required
def students_rating_by_subject(student_id, subject_id):
    student = User.query.get_or_404(student_id)
    subject = Subject.query.get_or_404(subject_id)
    full_name = get_full_name(student)
    subject_name = subject.name
    attendance_count_user, count_hours, attendance, labs_count_user, labs_count, labs, grade = \
        get_education_student_by_subject(student_id, subject_id)
    return render_template('rating_by_subject.html',
                           title='Рейтинг студента по предмету',
                           full_name=full_name,
                           subject_name=subject_name,
                           attendance_count_user=attendance_count_user,
                           count_hours=count_hours,
                           attendance=attendance,
                           labs_count_user=labs_count_user,
                           labs_count=labs_count,
                           labs=labs,
                           grade=grade
                           )


@deans_office.route('/admin')
@deans_office.route('/admin/<string:entity>')
@login_required
def admin(entity=None):
    import pointraing.deans_office.utils as utils
    groups = utils.get_entities()
    if not entity:
        entity = groups[0]['id']
    entities_values = utils.get_entities_values()
    if entity in entities_values:
        add_url, fields, entity_list_values = entities_values[entity]()
    else:
        flash('Ошибка, обратитесь к администратору системы', 'warning')
        return redirect(url_for('main.home'))
    return render_template('admin.html',
                           title='Администрирование',
                           entity=entity,
                           groups=groups,
                           fields=fields,
                           add_url=add_url,
                           entity_list_values=entity_list_values,
                           active_tab='admin')


@deans_office.route('/admin/<string:entity>/update', methods=['GET', 'POST'])
@deans_office.route('/admin/<string:entity>/<string:item_id>/update', methods=['GET', 'POST'])
@login_required
def entity_update(entity, item_id=None):
    import pointraing.deans_office.utils as utils
    title = 'Изменить запись' if item_id else 'Добавить запись'
    groups = utils.get_entities()
    method = '_'.join((entity, 'update'))
    if utils.__dict__[method]:
        return utils.__dict__[method](item_id, title, groups)
    else:
        return redirect('main.home')


@deans_office.route('/admin/<string:entity>/<string:item_id>/delete', methods=['GET'])
@login_required
def entity_remove(entity, item_id):
    import pointraing.deans_office.utils as utils
    method = '_'.join((entity, 'remove'))
    if utils.__dict__[method]:
        flash('Запись была удалена!', 'success')
        return utils.__dict__[method](item_id)
    else:
        return redirect('main.home')
