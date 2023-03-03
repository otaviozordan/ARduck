from flask import request, Response
from app import db, app
from app.models.user_table import Usuario
import json

@app.route('/registrar', methods=['POST'])
def registrar_acao():
    body = request.get_json()

    pwd = body['password']
    nome = body['nome']
    email = body['email']
    response = {}
    try:
        if nome and email and pwd:
            usuario = Usuario(password=pwd, nome=nome, email=email, turma=None)
            db.session.add(usuario)
            db.session.commit()
            print("Usuário Cadastrado.")
            response['create'] = True
            return Response(json.dumps(response), status=200, mimetype="application/json")
        if not nome:
            response['Mensagem'] = 'Nome nulo.'
        if not email:
            response['Mensagem'] = response['Mensagem'] + 'Email nulo.'
        if not pwd:
            response['Mensagem'] = response['Mensagem'] + 'Password nulo.'
        return Response(json.dumps(response), status=200, mimetype="application/json")
    
    except Exception as e:
        print('Erro', e, " ao cadastrar usuário.")
        response['create'] = False
        response['erro'] = str(e)
        return Response(json.dumps(response), status=400, mimetype="application/json")
