from pointraing import db
from flask import render_template, url_for, redirect, request, flash, abort, send_from_directory, current_app, Blueprint
from flask_login import current_user, login_required
from pointraing.students.forms import StudentActivityForm
from pointraing.models import Attendance, Lab, LabsGrade, Grade, AttendanceGrade, ActivityType, ActivitySubType, \
    RateActivity, Activity
import uuid
import os
import secrets

students = Blueprint('students', __name__, template_folder='templates', url_prefix='/students')


@students.route("/education")
@students.route("/education/<string:subject_id>")
@login_required
def education(subject_id=None):
    group = current_user.group
    attendance_subjects = Attendance.query.filter_by(group_id=group.id).group_by(Attendance.subject_id).all()
    subjects = []
    for i in attendance_subjects:
        subjects.append(i.subject)
    if not subject_id and len(subjects) > 0:
        subject_id = subjects[0].id

    if not subject_id:
        return render_template('education.html',
                               active_tab='education',
                               right_group=subjects,
                               group_id=subject_id
                               )
    else:
        attendance_user = AttendanceGrade.query \
            .filter(AttendanceGrade.user_id == current_user.id).subquery()
        attendance = Attendance.query \
            .filter(Attendance.subject_id == subject_id) \
            .filter(Attendance.group_id == current_user.group_id) \
            .add_columns(attendance_user.c.id, attendance_user.c.active) \
            .outerjoin(attendance_user, Attendance.id == attendance_user.c.attendance_id) \
            .order_by(Attendance.date).all()
        attendance_count_user = AttendanceGrade.query \
            .join(AttendanceGrade.attendance) \
            .filter(Attendance.subject_id == subject_id) \
            .filter(AttendanceGrade.user_id == current_user.id) \
            .count()
        labs_user_subq = LabsGrade.query \
            .filter(LabsGrade.user_id == current_user.id).subquery()
        labs = Lab.query \
            .filter(Lab.subject_id == subject_id) \
            .add_columns(labs_user_subq.c.id, labs_user_subq.c.date) \
            .outerjoin(labs_user_subq, Lab.id == labs_user_subq.c.lab_id) \
            .all()
        labs_count_user = LabsGrade.query \
            .join(Lab, LabsGrade.lab) \
            .filter(Lab.subject_id == subject_id) \
            .filter(LabsGrade.user_id == current_user.id) \
            .count()
        grade = Grade.query \
            .filter_by(user_id=current_user.id) \
            .filter_by(subject_id=subject_id).order_by(Grade.date).all()
        return render_template('education.html',
                               active_tab='education',
                               right_group=subjects,
                               group_id=subject_id,
                               count_hours=len(attendance),
                               attendance_count_user=attendance_count_user,
                               attendance=attendance,
                               labs=labs,
                               labs_count=len(labs),
                               labs_count_user=labs_count_user,
                               grade=grade
                               )


def get_students_activity():
    return ActivityType.query.all()


@students.route("/activity")
@students.route("/activity/<string:activity_id>")
@login_required
def activity(activity_id=None):
    activity = get_students_activity()
    if not activity_id and len(activity) > 0:
        activity_id = activity[0].id

    activity_by_user = Activity.query \
        .filter(Activity.user_id == current_user.id) \
        .filter(Activity.type_id == activity_id).all()
    return render_template('activity.html',
                           active_tab='activity',
                           right_group=activity,
                           group_id=activity_id,
                           activity_by_user=activity_by_user
                           )


def save_file(form_file):
    random_hex = secrets.token_hex(8)
    file = request.files[form_file.name]
    if file.filename == '':
        flash('Нет выбранного файла')
        return redirect(request.url)
    _, f_ext = os.path.splitext(file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

    file.save(picture_path)
    return picture_fn


def get_activity_sub_type_choices(activity_id):
    choices = []
    sub_type_id = None
    for g in RateActivity.query.filter(RateActivity.activity_type_id == activity_id):
        if g.sub_type:
            choices.append((g.id, g.sub_type.name))
        else:
            sub_type_id = g.id
    return {
        'choices': choices,
        'sub_type_id': sub_type_id
    }


@students.route("/activity/<string:activity_id>/new", methods=['GET', 'POST'])
@login_required
def activity_new(activity_id):
    form = StudentActivityForm()
    sub_type_choices = get_activity_sub_type_choices(activity_id)
    choices = sub_type_choices['choices']
    sub_type_id = sub_type_choices['sub_type_id']

    form.sub_type_id.choices = choices
    if form.validate_on_submit():
        picture_file = save_file(form.file)
        activity = Activity(
            id=uuid.uuid4().hex,
            name=form.name.data,
            file=picture_file,
            user_id=current_user.id,
            type_id=activity_id,
            rate_id=sub_type_id if sub_type_id else form.sub_type_id.data
        )
        db.session.add(activity)
        db.session.commit()
        flash('Ваша грамота принята на рассмотрение!', 'success')
        return redirect(url_for('students.activity', activity_id=activity_id))
    return render_template('activity_new.html',
                           title='Новая активная деятельность',
                           active_tab='activity',
                           right_group=get_students_activity(),
                           group_id=activity_id,
                           form=form
                           )


@students.route("/activity/<string:activity_id>/doc/<string:doc_id>/update", methods=['GET', 'POST'])
@login_required
def update_activity(activity_id, doc_id):
    doc = Activity.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        abort(403)
    form = StudentActivityForm()
    sub_type_choices = get_activity_sub_type_choices(activity_id)
    choices = sub_type_choices['choices']
    sub_type_id = sub_type_choices['sub_type_id']

    form.sub_type_id.choices = choices
    if form.validate_on_submit():
        doc.name = form.name.data
        picture_file = save_file(form.file)
        doc.file = picture_file
        doc.rate_id = sub_type_id if sub_type_id else form.sub_type_id.data
        db.session.commit()
        flash('Ваша грамота обновлена!', 'success')
        return redirect(url_for('students.activity', activity_id=activity_id))
    elif request.method == 'GET':
        form.name.data = doc.name
        form.file.data = send_from_directory(current_app.config['UPLOAD_FOLDER'], doc.file)
        if not sub_type_id:
            form.sub_type_id.data = doc.rate_id
    return render_template('activity_new.html',
                           title='Редактирование активной деятельности',
                           active_tab='activity',
                           right_group=get_students_activity(),
                           group_id=activity_id,
                           form=form
                           )


@students.route("/activity/<string:activity_id>/doc/<string:doc_id>/delete", methods=['GET'])
@login_required
def delete_activity(activity_id, doc_id):
    doc = Activity.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        abort(403)
    db.session.delete(doc)
    db.session.commit()
    flash('Ваша грамота была удалена!', 'success')
    return redirect(url_for('students.activity', activity_id=activity_id))

