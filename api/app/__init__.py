from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pymongo

app = Flask(__name__)

app.secret_key = 'super secret key'

try:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/arduck'
    db = SQLAlchemy(app)

    mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
    mongoDB = mongoClient["ARduck"]

except Exception as e:
    print('Erro', e, " ao cadastrar conectar aos Databases.")
    
login_manager = LoginManager(app)
login_manager.init_app(app)

from app.controllers.imagens import imgsRec
from app.controllers.user import user_control_routes
from app.controllers.user import user_login_routes
from app.controllers.quiz import quiz_routes
from app.controllers import home_routes
from app.controllers.trilha import trilhas_control_routes