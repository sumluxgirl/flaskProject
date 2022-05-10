from pointraing import db
from datetime import datetime

labs_grade = db.Table('labs_grade',
                      db.Column('lab_id', db.String, db.ForeignKey('lab.id'), primary_key=True),
                      db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('student_id', db.String, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('date', db.DateTime, nullable=False, default=datetime.utcnow)
                      )


class Role(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "Role('{self.name}')"


class User(db.Model):
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

    def __repr__(self):
        return "User('{self.name}', 'self.login')"


class Group(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', backref='group', lazy=True)

    def __repr__(self):
        return "Group('{self.name}')"


class Subject(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    count_hours = db.Column(db.Integer, nullable=False)
    labs = db.relationship('Lab', backref='subject', lazy=True)

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


class AttendanceType(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "AttendanceType('{self.name}')"


class Attendance(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    subject_id = db.Column(db.String(32), db.ForeignKey('subject.id'), nullable=False)
    group_id = db.Column(db.String(32), db.ForeignKey('group.id'), nullable=False)
    type_id = db.Column(db.String(32), db.ForeignKey('attendance_type.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Attendance('{self.student_id}', '{self.active}')"


class AttendanceGrade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "AttendanceGrade('{self.student_id}', '{self.active}')"


class TypeGrade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "TypeGrade('{self.name}')"


class Grade(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.String(32), db.ForeignKey('subject.id'), nullable=False)
    value = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type_id = db.Column(db.String(32), db.ForeignKey('type_grade.id'), nullable=False)

    def __repr__(self):
        return "Grade('{self.name}', '{self.student_id}', '{self.value}')"


class Activity(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    student_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(240), nullable=True)
    type_id = db.Column(db.String(32), db.ForeignKey('activity_type.id'), nullable=False)
    rate_id = db.Column(db.String(32), db.ForeignKey('rate_activity.id'), nullable=False)

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
    activity_sub_type_id = db.Column(db.String(32), db.ForeignKey('activity_sub_type.id'), nullable=False)
    value = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "RateActivity('{self.activity_type_id}', '{self.activity_sub_type_id}', '{self.value}')"
