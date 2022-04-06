
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import config

DB_NAME = config.LOCAL_DB_NAME
DB_HOST = config.LOCAL_DB_HOST
DB_USER = config.LOCAL_DB_USERNAME
DB_PASSWORD = config.LOCAL_DB_PASSWORD

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + DB_USER + ':' + '' + DB_HOST + DB_NAME
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# tell the login manager where is the login route
login_manager.login_view = 'login'
# change the messages style from login manager
login_manager.login_message_category = 'info'

from bloga import routes

db.create_all()
db.session.commit()