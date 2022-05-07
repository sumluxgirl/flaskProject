from pointraing import db
from datetime import datetime


class Role(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "Role('{self.name}')"


class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role_id = db.Column(db.String, db.ForeignKey('role.id'), nullable=False)
    group_id = db.Column(db.String, db.ForeignKey('group.id'), nullable=True)

    def __repr__(self):
        return "User('{self.name}', 'self.login')"


class Group(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    users = db.relationship('User', backref='group', lazy=True)

    def __repr__(self):
        return "Group('{self.name}')"


class Subject(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    count_hours = db.Column(db.Integer, nullable=False)
    labs = db.relationship('Lab', backref='subject', lazy=True)

    def __repr__(self):
        return "Subject('{self.name}')"


class Lab(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject_id = db.Column(db.String(20), db.ForeignKey('subject.id'), nullable=False)

    def __repr__(self):
        return "Lab('{self.name}')"

labs_grade = db.Table('labs_grade',
                      db.Column('lab_id', db.String, db.ForeignKey('lab.id'), primary_key=True),
                      db.Column('user_id', db.String, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('student_id', db.String, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('value', db.Boolean, nullable=False, default=False),
                      db.Column('date', db.DateTime, nullable=False, default=datetime.utcnow)
                      )
