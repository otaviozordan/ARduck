from app import db,app

class Questoes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    colecao = db.Column(db.String(50), nullable=False)
    titulo = db.Column(db.String(50), nullable=False)
    texto = db.Column(db.String(244), nullable=False)
    imgPath = db.Column(db.String(50), default=None)
    respostaCorreta = db.Column(db.String(50), nullable=False)
    alternativa1 = db.Column(db.String(50))
    alternativa2 = db.Column(db.String(50))
    alternativa3 = db.Column(db.String(50))
    alternativa4 = db.Column(db.String(50))

    def __init__(self, colecao, titulo, texto, imgPath, respostaCorreta, alternativa1, alternativa2, alternativa3, alternativa4):
        self.colecao = colecao
        self.titulo = titulo
        self.texto = texto
        self.imgPath = imgPath
        self.respostaCorreta = respostaCorreta
        self.alternativa1 = alternativa1
        self.alternativa2 = alternativa2
        self.alternativa3 = alternativa3
        self.alternativa4 = alternativa4

    def to_json(self):
        return {
                "id": self.id,
                "colecao": self.colecao,
                "titulo": self.titulo,
                "texto": self.texto,
                "imgPath": self.imgPath,
                "respostaCorreta": self.respostaCorreta,
                "alternativa1": self.alternativa1,
                "alternativa2": self.alternativa2,
                "alternativa3": self.alternativa3,
                "alternativa4": self.alternativa4
             }

def verificarRespostaCorreta(id, respostaDoUsuario):
        Questao = Questoes.query.filter_by(id=id).first()
        if Questao.respostaCorreta == respostaDoUsuario:
             return True
        else:
             return False

def create_quiz_table():
    with app.app_context():
        db.create_all()

def delete_quiz_table():
    with app.app_context():
        questoes_objeto = Questoes.query.all()
        for questao_objeto in questoes_objeto:
            db.session.delete(questao_objeto)
            db.session.commit()