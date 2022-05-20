from pointraing import app, bcrypt, db
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from pointraing.forms import LoginForm, ResetPasswordForm, StudentActivityForm
from pointraing.models import User, Attendance, Lab, LabsGrade, Grade, AttendanceGrade, ActivityType, ActivitySubType, \
    RateActivity, Activity
import uuid
import os
import secrets


@app.route("/")
@app.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role.name == 'Студент':
        return redirect(url_for('student_education'))
    return render_template('home.html')


@app.route("/student/education")
@app.route("/student/education/<string:subject_id>")
@login_required
def student_education(subject_id=None):
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


@app.route("/student/activity")
@app.route("/student/activity/<string:activity_id>")
@login_required
def student_activity(activity_id=None):
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
    picture_path = os.path.join(app.root_path, 'static/activity_files', picture_fn)

    file.save(picture_path)
    return picture_fn


@app.route("/student/activity/<string:activity_id>/new", methods=['GET', 'POST'])
@login_required
def student_activity_new(activity_id):
    form = StudentActivityForm()
    choices = []
    sub_type_id = None
    for g in RateActivity.query.filter(RateActivity.activity_type_id == activity_id):
        if g.sub_type:
            choices.append((g.id, g.sub_type.name))
        else:
            sub_type_id = g.id

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
        return redirect(url_for('student_activity', activity_id=activity_id))
    return render_template('activity_new.html',
                           title='Новая активная деятельность',
                           active_tab='activity',
                           right_group=get_students_activity(),
                           group_id=activity_id,
                           form=form,
                           legend='Новая активная деятельность'
                           )


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте логин и пароль', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    user_name_tuple = (current_user.surname, current_user.name, current_user.patronymic)
    full_name = ' '.join(user_name_tuple)
    role = current_user.role.name
    group = current_user.group
    group_name = group.name if group else None
    print(current_user.get_reset_token())
    return render_template('account.html', title='Account', full_name=full_name, role=role, group_name=group_name)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Недействительный или просроченный токен', 'warning')
        return redirect(url_for('account'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Пароль был изменен', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
