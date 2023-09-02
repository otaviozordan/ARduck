from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from colorama import Fore, Style 
import mysql.connector
import pymongo
import logging
from sqlalchemy.exc import SQLAlchemyError 

# Configura o nível de log global para DEBUG
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# Função para formatar mensagens de erro
def erro_msg(msg, error):
    return f"{Fore.RED}[ERRO]{Style.RESET_ALL} {msg} - {error}"

# Configura o Flask
app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'
DATABASE_IMG_PATH = 'api\\app\\models\\imgs\\'

# Configura o SQLAlchemy
try:   
    from app.models import criar_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/arduck'
    db = SQLAlchemy(app)

    # Configura o MongoDB
    mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
    mongoDB = mongoClient["ARduck"]
   
except SQLAlchemyError as e:  # Captura exceções do SQLAlchemy
    print(erro_msg("Erro ao conectar no DATABASE (SQLAlchemyError)", e))
    logging.error("Erro ao conectar no DATABASE (SQLAlchemyError): %s", e)

except mysql.connector.Error as e:  # Captura exceções do MySQL
    print(erro_msg("Erro ao conectar no DATABASE (mysql.connector.Error)", e))
    logging.error("Erro ao conectar no DATABASE (mysql.connector.Error): %s", e)

except Exception as e:
    print(erro_msg("Erro ao conectar no DATABASE", e))
    logging.error("Erro ao conectar no DATABASE: %s", e)

# Configura o LoginManager
login_manager = LoginManager(app)
login_manager.init_app(app)

# Importa os controladores e rotas
from app.controllers.imagens import imgsRec
from app.controllers.user import user_control_routes
from app.controllers.user import user_login_routes
from app.controllers.quiz import quiz_routes
from app.controllers.quiz import quiz_respostas_abertas
from app.controllers.trilha import trilhas_control_routes
from app.controllers.site import routes

# Redefinir cores ao final
print(Style.RESET_ALL)
