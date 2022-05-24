from pointraing import create_app, db
from data import create_default_values
from flask import current_app

app = create_app()


def adding_data():
    with app.app_context():
        if current_app.config["ENV"] == 'development':
            db.drop_all()
            create_default_values()


if __name__ == '__main__':
    app.run(debug=True)
    # adding_data() #Run on first

