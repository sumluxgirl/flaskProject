from flask import Blueprint, render_template
from flask_login import login_required
from pointraing.models import Subject

tutors = Blueprint('tutors', __name__, template_folder='templates', url_prefix='/tutors')


@tutors.route("/subjects")
@login_required
def subjects():
    subjects_list = Subject.query.all()
    return render_template('subjects.html',
                           title="Учебные предметы",
                           subjects=subjects_list
                           )
