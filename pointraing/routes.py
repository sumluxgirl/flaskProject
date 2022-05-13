from pointraing import app
from flask import render_template, url_for

@app.route("/")
@app.route("/home")
def hello_world():
    return render_template('home.html')
