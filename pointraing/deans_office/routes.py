from flask import Blueprint, render_template
from flask_login import current_user, login_required

dean_office = Blueprint('dean_office', __name__, template_folder='templates')


@dean_office.route('/rating')
@login_required
def rating():
    return render_template('rating.html')
