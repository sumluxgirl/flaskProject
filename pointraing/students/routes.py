from pointraing import db
from flask import render_template, url_for, redirect, request, flash, abort, send_from_directory, current_app, Blueprint
from flask_login import current_user, login_required
from pointraing.students.forms import StudentActivityForm
from pointraing.models import Attendance, ActivityType, RateActivity, Activity
from pointraing.main.utils import get_education_student_by_subject, is_student
import uuid
import os
import secrets

students = Blueprint('students', __name__, template_folder='templates', url_prefix='/students')


def check_on_rights():
    if not is_student():
        abort(403)


@students.route("/education")
@students.route("/education/<string:subject_id>")
@login_required
def education(subject_id=None):
    check_on_rights()
    group = current_user.group
    attendance_subjects = Attendance.query.filter_by(group_id=group.id).group_by(Attendance.subject_id).limit(100).all()
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
        attendance_count_user, count_hours, attendance, labs_count_user, labs_count, labs, grade, auto_grade = \
            get_education_student_by_subject(current_user.id, subject_id)

        return render_template('education.html',
                               active_tab='education',
                               right_group=subjects,
                               group_id=subject_id,
                               count_hours=count_hours,
                               attendance_count_user=attendance_count_user,
                               attendance=attendance,
                               labs=labs,
                               labs_count=labs_count,
                               labs_count_user=labs_count_user,
                               grade=grade,
                               auto_grade=auto_grade
                               )


def get_students_activity():
    return ActivityType.query.limit(100).all()


@students.route("/activity")
@students.route("/activity/<string:activity_id>")
@login_required
def activity(activity_id=None):
    check_on_rights()
    activity_list = get_students_activity()
    if not activity_id and len(activity_list) > 0:
        activity_id = activity_list[0].id

    activity_by_user = Activity.query \
        .filter(Activity.user_id == current_user.id) \
        .filter(Activity.type_id == activity_id).limit(100).all()
    return render_template('activity.html',
                           active_tab='activity',
                           right_group=activity_list,
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
    check_on_rights()
    form = StudentActivityForm()
    sub_type_choices = get_activity_sub_type_choices(activity_id)
    choices = sub_type_choices['choices']
    sub_type_id = sub_type_choices['sub_type_id']

    form.sub_type_id.choices = choices
    if form.validate_on_submit():
        picture_file = save_file(form.file)
        db.session.add(Activity(
            id=uuid.uuid4().hex,
            name=form.name.data,
            file=picture_file,
            user_id=current_user.id,
            type_id=activity_id,
            rate_id=sub_type_id if sub_type_id else form.sub_type_id.data
        ))
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
    check_on_rights()
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
    check_on_rights()
    doc = Activity.query.get_or_404(doc_id)
    if doc.user_id != current_user.id:
        abort(403)
    db.session.delete(doc)
    db.session.commit()
    flash('Ваша грамота была удалена!', 'success')
    return redirect(url_for('students.activity', activity_id=activity_id))
