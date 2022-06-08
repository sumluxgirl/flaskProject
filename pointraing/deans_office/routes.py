from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from pointraing.models import Group, User, Attendance, Activity, AttendanceGrade, Lab, LabsGrade, Grade, GradeUsers, \
    TypeGrade
from pointraing.main.routes import get_full_name
from pointraing import db
from pointraing.deans_office.forms import DeclineActivityForm

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
    attendance_sq = Attendance.query.filter_by(group_id=group_id)
    attendance_subjects = attendance_sq.group_by(Attendance.subject_id).all()
    subjects = []
    for i in attendance_subjects:
        subject = i.subject
        subject_id = subject.id
        attendance_count = 0
        lab_count = 0
        grade_count = 0
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
        lab_sq = Lab.query.with_entities(Lab.id).filter(Lab.subject_id == subject_id)
        lab_user = LabsGrade.query \
            .filter(LabsGrade.user_id == student_id) \
            .filter(LabsGrade.lab_id.in_(lab_sq)).all()
        for item_lab_user in lab_user:
            if (item_lab_user.date - item_lab_user.lab.deadline).total_seconds() < 0:
                lab_count = lab_count + 2
            else:
                lab_count = lab_count + 1
        grade_sq = Grade.query.with_entities(Grade.id).filter(Grade.subject_id == subject_id)
        grade_type_sq = grade_sq.join(Grade.type).group_by(Grade.id)
        grade_user = GradeUsers.query \
            .with_entities(GradeUsers.value) \
            .filter(GradeUsers.user_id == student_id) \
            .filter(GradeUsers.grade_id.in_(grade_sq)).all()
        for item_grade_user in grade_user:
            grade_count = grade_count + item_grade_user.value

        attendance_max_count = subject.count_hours * 2
        lab_max_count = lab_sq.count() * 2
        grade_max_count = grade_type_sq.filter(TypeGrade.name == 'Экзамен').count() * 5 + grade_type_sq.filter(
            TypeGrade.name == 'Зачет').count()
        subjects.append({
            'id': subject_id,
            'name': subject.name,
            'attendance_max_count': attendance_max_count,
            'attendance_count': attendance_count,
            'lab_max_count': lab_max_count,
            'lab_count': lab_count,
            'grade_max_count': grade_max_count,
            'grade_count': grade_count,
            'count': attendance_count + lab_count + grade_count,
            'max_count': attendance_max_count + lab_max_count + grade_max_count
        })
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
