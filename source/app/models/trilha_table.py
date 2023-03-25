from app import db,app

class Trilhas (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Inter, nullable=False)
    titulo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    turma = db.Column(db.String(50), default='1')

    def __init__(self, username, password, nome, email, turma):
        self.username = username
        self.nome = nome
        self.email = email
        self.turma = turma

def create_trilhas_table():
    with app.app_context():
        db.create_all()