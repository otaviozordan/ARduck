from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/arduck'
db = SQLAlchemy(app)

login_manager = LoginManager(app)

from app.controllers.user import user_control_routes
from app.controllers.user import user_login_routes
from app.controllers.quiz import quiz_routes
