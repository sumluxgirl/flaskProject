from pointraing import db, login_manager
from jwt import encode as encode_jwt, decode as decode_jwt, ExpiredSignatureError, InvalidTokenError
from flask_login import UserMixin
from datetime import datetime, timedelta
from flask import flash, current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Role(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "Role('{self.name}')"


class User(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    patronymic = db.Column(db.String(120), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.String, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    group_id = db.Column(db.String, db.ForeignKey('group.id'), nullable=True)

    # labs = db.relationship('Labs', secondary=labs_grade, lazy='subquery',
    #                        backref=db.backref('users', lazy=True))

    def get_reset_token(self, expires_sec=1800):
        """
           Generates the Auth Token
           :return: string
           """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=expires_sec),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            return encode_jwt(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = decode_jwt(token, current_app.config.get('SECRET_KEY'), algorithms=["HS256"])['sub']
            return User.query.get(user_id)
        except ExpiredSignatureError:
            flash('Signature expired. Please log in again.')
            return None
        except InvalidTokenError as e:
            flash('Invalid token. Please log in again')
            return e

    def __repr__(self):
        return "User('{self.name}', 'self.login')"


class Group(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', backref='group', lazy='dynamic')

    def __repr__(self):
        return "Group('{self.name}')"


class Subject(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    count_hours = db.Column(db.Integer, nullable=False)
    labs = db.relationship('Lab', backref='subject', lazy=True)
    attendance = db.relationship('Attendance', backref='subject', lazy=True)

    def __repr__(self):
        return "Subject('{self.name}')"


class Lab(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject_id = db.Column(db.String(32), db.ForeignKey('subject.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "Lab('{self.name}')"


class LabsGrade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    lab_id = db.Column(db.String(32), db.ForeignKey('lab.id'), nullable=False)
    lab = db.relationship('Lab',
                          backref=db.backref('labs_grade', lazy=True))
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('labs_grade', lazy=True))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Lab('{self.lab_id}', '{self.user_id}')"


class AttendanceType(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "AttendanceType('{self.name}')"


class Attendance(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    subject_id = db.Column(db.String(32), db.ForeignKey('subject.id'), nullable=False)
    group_id = db.Column(db.String(32), db.ForeignKey('group.id'), nullable=False)
    group = db.relationship('Group',
                            backref=db.backref('attendance', lazy='dynamic'))
    type_id = db.Column(db.String(32), db.ForeignKey('attendance_type.id'), nullable=False)
    type = db.relationship('AttendanceType',
                           backref=db.backref('attendance', lazy=True))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Attendance('{self.subject_id}', '{self.type_id}')"


class AttendanceGrade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User',
                           backref=db.backref('attendance_grade', lazy=True))
    attendance_id = db.Column(db.String(32), db.ForeignKey('attendance.id'), nullable=False)
    attendance = db.relationship('Attendance',
                                 backref=db.backref('attendance_grade', lazy=True))
    active = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "AttendanceGrade('{self.user_id}', '{self.active}')"


class TypeGrade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "TypeGrade('{self.name}')"


class Grade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    subject_id = db.Column(db.String(32), db.ForeignKey('subject.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type_id = db.Column(db.String(32), db.ForeignKey('type_grade.id'), nullable=False)

    def __repr__(self):
        return "Grade('{self.name}', '{self.subject_id}', '{self.type_id}')"


class GradeUsers(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    grade_id = db.Column(db.String(32), db.ForeignKey('grade.id'), nullable=False)
    value = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "Grade('{self.grade_id}', '{self.user_id}', '{self.value}')"


class Activity(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(240), nullable=True)
    type_id = db.Column(db.String(32), db.ForeignKey('activity_type.id'), nullable=False)
    rate_id = db.Column(db.String(32), db.ForeignKey('rate_activity.id'), nullable=False)
    rate = db.relationship('RateActivity',
                           backref=db.backref('activity', lazy=True))

    def __repr__(self):
        return "Activity('{self.name}', '{self.user_id}', '{self.file}')"


class ActivityType(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "ActivityType('{self.name}')"


class ActivitySubType(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "ActivitySubType('{self.name}')"


class RateActivity(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    activity_type_id = db.Column(db.String(32), db.ForeignKey('activity_type.id'), nullable=False)
    type = db.relationship('ActivityType',
                           backref=db.backref('rate', lazy=True))
    activity_sub_type_id = db.Column(db.String(32), db.ForeignKey('activity_sub_type.id'), nullable=True)
    sub_type = db.relationship('ActivitySubType',
                               backref=db.backref('rate', lazy=True))
    value = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "RateActivity('{self.activity_type_id}', '{self.activity_sub_type_id}', '{self.value}')"
