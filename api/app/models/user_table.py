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
    password = db.Column(db.String(150), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    turma = db.Column(db.String(50), default='default')
    privilegio = db.Column(db.String(50), default='usuario')

    def __init__(self, password, nome, email, turma, privilegio):
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

def delete_login_table():
    with app.app_context():
        usuarios_obj = Usuario.query.all()
        for usuario_obj in usuarios_obj:
            db.session.delete(usuario_obj)
            db.session.commit()

def authenticate(privilegio, redirect=False):
    response = {}
    usuario = current_user.is_authenticated
    if usuario: 
        usuario = current_user
        if (usuario.privilegio == privilegio):
            return False
        elif(privilegio == "log"):
            return False
        elif(usuario.privilegio == "administrador"):
            return False
        else:
            response['Acesso'] = "negado"
            response['Necessario'] = privilegio
    else:
        response['Acesso'] = "negado"
        response['Necessario'] = "Estar logado"
    return response

#Usar:
#    auth = authenticate("adm")
#    if auth:
#        return Response(json.dumps(auth), status=200, mimetype="application/json")