from flask import Flask

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
import pymongo

app = Flask(__name__)

app.secret_key = 'super secret key'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/arduck'
db = SQLAlchemy(app)

mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
mongoDB = mongoClient["ARduck"]
colectionTrilhas = mongoDB["Trilhas"]

login_manager = LoginManager(app)
login_manager.init_app(app)

from app.controllers.user import user_control_routes
from app.controllers.user import user_login_routes
from app.controllers.quiz import quiz_routes
from app.controllers.trilha import home_routes
from app.controllers.trilha import trilhas_control_routes