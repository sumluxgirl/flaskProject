from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from pointraing.models import Group, User, Subject, Attendance, Activity
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
            return redirect('main.home')
    else:
        current_group = Group.query.get_or_404(group_id)
        if not current_group:
            flash('Выбранной группы не существует, обратитесь к администратору системы', 'warning')
            return redirect('main.home')
    students_list = current_group.users.all()
    if not student_id:
        if len(students_list) > 0:
            select_user = students_list[0]
            student_id = select_user.id
        else:
            flash('Студентов в этой группе пока не существует, обратитесь к администратору системы', 'warning')
            return redirect('main.home')
    else:
        select_user = current_group.users.filter(User.id == student_id).first()
        if not select_user:
            flash('Выбранной группе такого студента не существует, обратитесь к администратору системы', 'warning')
            return redirect('main.home')
    students = []
    for item in students_list:
        students.append({
            'id': item.id,
            'name': get_full_name(item)
        })
    attendance_subjects = Attendance.query.filter_by(group_id=group_id).group_by(Attendance.subject_id).all()
    subjects = []
    for i in attendance_subjects:
        subjects.append(i.subject)
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
    if not activity:
        flash('Выбранной активной деяотельности не существует, обратитесь к администратору системы', 'warning')
        return redirect('main.home')
    activity.status = True
    db.session.commit()
    flash('Активность обновлена!', 'success')
    return redirect(url_for('deans_office.rating', group_id=group_id, student_id=student_id))


@deans_office.route('/activity/<string:activity_id>/group/<string:group_id>/student/<string:student_id>/decline',
                    methods=['GET', 'POST'])
@login_required
def activity_decline(activity_id, group_id, student_id):
    activity = Activity.query.get_or_404(activity_id)
    if not activity:
        flash('Выбранной активной деяотельности не существует, обратитесь к администратору системы', 'warning')
        return redirect('main.home')
    form = DeclineActivityForm()
    if form.validate_on_submit():
        activity.status = False
        activity.comment = form.comment.data
        db.session.commit()
        flash('Активность обновлена!', 'success')
        return redirect(url_for('deans_office.rating', group_id=group_id, student_id=student_id))
    # return render_template('main.home')
    return redirect('main.home')


