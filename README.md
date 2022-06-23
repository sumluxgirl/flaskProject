# flaskProject
Point rating system USATU
## database scheme
![Alt-текст](https://github.com/sumluxgirl/flaskProject/blob/main/scoring%20system.pdf)
## Create environment
```
    py -3 -m venv venv
```
## Activate the environment
```
    venv\Scripts\activate
```
## Installation
###Windows
```
    pip install Flask
    pip install -U Flask-SQLAlchemy
    pip install flask-bcrypt
    pip install flask-login
    pip install -U Flask-WTF
    pip install pyjwt
    pip install pymysql
    cd pointrating/static
    npm i bootstrap-icons
```
###Linux
```
    git clone https://github.com/sumluxgirl/flaskProject.git
    cd flaskProject
    python3 -m venv venv
    . venv/bin/activate
    pip install Flask
    pip install -U Flask-SQLAlchemy
    pip install flask-bcrypt
    pip install flask-login
    pip install -U Flask-WTF
    pip install pyjwt
    pip install pymysql
    cd pointraing/static
    npm i bootstrap-icons
```
##quick start
```
    set FLASK_APP=app.py
    set FLASK_ENV=development
    py -m flask run
```