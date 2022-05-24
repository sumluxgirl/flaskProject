from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/activity_files')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from pointraing.main.routes import main
    from pointraing.users.routes import users
    from pointraing.students.routes import students
    from pointraing.tutors.routes import tutors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(students)
    app.register_blueprint(tutors)
    return app
