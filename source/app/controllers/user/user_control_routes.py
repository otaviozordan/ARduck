from flask import request, Response
from app import db, app
from app.models.user_table import Usuario
import json

@app.route('/registrar', methods=['POST'])
def registrar_acao():
    body = request.get_json()

    try:
        username = body['username']
        pwd = body['password']
        nome = body['nome']
        email = body['email']

        if ('turma' in body):
            turma = body['turma']
        else :
            turma = None

        response = {}
        try:
            if nome and email and pwd:
                usuario = Usuario(username=username, password=pwd, nome=nome, email=email, turma=turma)   
                db.session.add(usuario)
                db.session.commit()

                print("Usuário Cadastrado.")
                response['create'] = True
                return Response(json.dumps(response), status=200, mimetype="application/json")
    
        except Exception as e:
            print('Erro', e, " ao cadastrar usuário.")
            response['create'] = False
            response['erro'] = str(e)
            
            return Response(json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {'Retorno': "Parametros invalidos ou ausentes", 'erro': str(e)}
    
        return Response(json.dumps(response), status=400, mimetype="application/json")
