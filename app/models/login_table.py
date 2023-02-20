from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def get_user(user_id):
    return Usuario.query.filter_by(id=user_id)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    turma = db.Column(db.String(50))

    def __init__(self, username, password, nome, email, turma):
        self.username = username
        self.password = generate_password_hash(password)
        self.nome = nome
        self.email = email
        self.turma = turma

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return "<User %r>" % self.username
    

#class Circuitos(db.Model):
#    __tablename__ = 'circuitos'
#
#    id = db.Column(db.Integer, primary_key=True)
#    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'))

