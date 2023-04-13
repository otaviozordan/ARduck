from app import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask import Response
import json

@login_manager.user_loader
def get_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    turma = db.Column(db.String(50), default='1')
    privilegio = db.Column(db.String(50), default='usuario')

    def __init__(self, password, nome, email, turma, privilegio):
        self.id = id 
        self.password = generate_password_hash(password)
        self.nome = nome
        self.email = email
        self.turma = turma
        self.privilegio = privilegio

    def to_json(self):
        return {
                "id": self.id,
                "password": self.password,
                "nome": self.nome,
                "email": self.email,
                "turma": self.turma,
                "privilegio":self.privilegio
             }

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    @property 
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return "<User %r>" % self.nome

def create_login_table():
    with app.app_context():
        db.create_all()

def authenticate(privilegio_necessario): #Nãop funciona
    authe = current_user.is_authenticated
    print (authe)
    try:
        usuario = current_user
        privilegio_user = usuario.privilegio
        print (privilegio_user)
        if (privilegio_user == privilegio_necessario):
            return
        else:
            response = {"Acesso": "Negado", "Necessario":str(privilegio_necessario)}
            return Response(json.dumps(response), status=200, mimetype="application/json") 
    except:
        response = {"Login": "Negado"}
        return Response(json.dumps(response), status=200, mimetype="application/json") 

def delete_login_table():
    with app.app_context():
        usuarios_obj = Usuario.query.all()
        for usuario_obj in usuarios_obj:
            db.session.delete(usuario_obj)
            db.session.commit()