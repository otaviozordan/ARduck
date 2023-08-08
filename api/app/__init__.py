from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import pymongo

app = Flask(__name__, template_folder='templates')

app.secret_key = 'super secret key'
DATABASE_IMG_PATH = 'api\\app\\models\\imgs\\'

try:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/arduck'
    db = SQLAlchemy(app)

    mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
    mongoDB = mongoClient["ARduck"]
   
except Exception as e:
    print("[ERRO] Erro ao conectar no DATABASE / ", e)
    
login_manager = LoginManager(app)
login_manager.init_app(app)

from app.controllers.imagens import imgsRec
from app.controllers.user import user_control_routes
from app.controllers.user import user_login_routes
from app.controllers.quiz import quiz_routes
from app.controllers.quiz import quiz_respostas_abertas
from app.controllers import home_routes
from app.controllers.trilha import trilhas_control_routes
from app.controllers import routes