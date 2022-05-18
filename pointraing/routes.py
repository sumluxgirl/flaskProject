from pointraing import app, bcrypt, db
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from pointraing.forms import LoginForm, ResetPasswordForm
from pointraing.models import User, Attendance, Lab, LabsGrade, Grade, Subject, AttendanceGrade


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

    if not subject_id:
        return render_template('education.html',
                               active_tab='education',
                               right_group=subjects,
                               group_id=subject_id
                               )
    else:
        current_subject = Subject.query.filter_by(id=subject_id).first()
        attendance = Attendance.query \
            .join(AttendanceGrade, Attendance.attendance_grade) \
            .add_entity(AttendanceGrade).from_self() \
            .filter(Attendance.subject_id == subject_id) \
            .filter(AttendanceGrade.user_id == current_user.id) \
            .order_by(Attendance.date).all()
        attendance_count_user = AttendanceGrade.query\
            .join(AttendanceGrade.attendance) \
            .filter(Attendance.subject_id == subject_id) \
            .filter(AttendanceGrade.user_id == current_user.id)\
            .count()
        labs = Lab.query\
            .join(LabsGrade, Lab.labs_grade) \
            .add_entity(LabsGrade).from_self() \
            .filter(Lab.subject_id == subject_id) \
            .filter(LabsGrade.user_id == current_user.id) \
            .all()
        labs_count_user = LabsGrade.query \
            .join(Lab, LabsGrade.lab) \
            .filter(Lab.subject_id == subject_id) \
            .filter(LabsGrade.user_id == current_user.id) \
            .count()
        grade = Grade.query.filter_by(user_id=current_user.id)\
            .filter_by(subject_id=subject_id).order_by(Grade.date).all()
        return render_template('education.html',
                               active_tab='education',
                               right_group=subjects,
                               group_id=subject_id,
                               count_hours=current_subject.count_hours,
                               attendance_count_user=attendance_count_user,
                               attendance=attendance,
                               labs=labs,
                               labs_count=len(labs),
                               labs_count_user=labs_count_user,
                               grade=grade
                               )


@app.route("/student/activity")
def student_activity():
    return render_template('student.html', active_tab='activity')


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
